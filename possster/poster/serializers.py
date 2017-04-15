from rest_framework import serializers
from poster.models import Poster
from django.contrib.auth.models import User


class PosterSerializer(serializers.HyperlinkedModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')

    class Meta:
        model = Poster
        fields = ('url', 'id', 'title', 'image', 'writer', 'content', 'created', 'modified', 'end')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')

