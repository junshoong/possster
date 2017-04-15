from poster.models import Poster
from poster.serializers import UserSerializer
from poster.serializers import PosterSerializer
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions


class PosterViewSet(viewsets.ModelViewSet):
    """
    `list`, `create`, `retrieve`, `update`, `destroy`
    """
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `detail` action
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
