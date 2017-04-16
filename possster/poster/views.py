from poster.models import Poster
from poster.serializers import UserSerializer
from poster.serializers import PosterSerializer
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
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
    """
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    @detail_route(renderer_classes=[JPEGRenderer])
    def get_post(self, request, *args, **kwargs):
        poster = self.get_object()
        return Response(poster.image)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `detail` action
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
