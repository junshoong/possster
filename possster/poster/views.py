from django.contrib.auth.models import User
from poster.models import Poster
from poster.serializers import UserSerializer
from poster.serializers import PosterSerializer
from poster.permissions import IsWriterOrReadOnly
from poster.permissions import IsUserSelf
from poster.permissions import IsUserSelfOrAdminUser
from poster.permissions import IsAnonymousUser
from poster.utils import EmailAuthTokenGenerator
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated


class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class PosterViewSet(viewsets.ModelViewSet):
    """
    `list`, `create`, `retrieve`, `update`, `destroy`
    and `image` action
    """
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    parser_classes = (FormParser, MultiPartParser, )
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
        IsWriterOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user, image=self.request.data.get('image'))

    @detail_route(renderer_classes=[JPEGRenderer])
    def image(self, request, *args, **kwargs):
        poster = self.get_object()
        return Response(poster.image)


class UserViewSet(viewsets.ModelViewSet):
    # `list` and `detail` action
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.BasePermission, )

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        elif self.request.method == 'POST':
            return [IsAnonymousUser()]
        elif self.request.method in ('PUT', 'PATCH',):
            return [IsUserSelf()]
        else:
            return [IsUserSelfOrAdminUser()]

    def list(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_active and not user.is_staff:
            queryset = User.objects.filter(id=user.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        if user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response()


@api_view(['GET'])
def verify_view(request, token):
    u = request.user
    e = EmailAuthTokenGenerator()

    # Require login
    if u.is_anonymous:
        raise NotAuthenticated

    # Token fail
    if not e.check_token(request.user, token):
        raise NotAuthenticated

    return Response()
