from poster.models import Poster
from poster.serializers import UserSerializer
from poster.serializers import PosterSerializer
from poster.serializers import UserUpdateSerializer
from poster.serializers import UserCreateSerializer
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import detail_route
from rest_framework.response import Response


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

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

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = UserUpdateSerializer
        elif self.request.method == 'POST':
            serializer_class = UserCreateSerializer

        return serializer_class

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        elif self.request.method == 'POST':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]
