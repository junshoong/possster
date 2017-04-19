from rest_framework import serializers
from poster.models import Poster
from django.contrib.auth.models import User


class PosterSerializer(serializers.HyperlinkedModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    image = serializers.ImageField(write_only=True, required=True)
    image_url = serializers.HyperlinkedIdentityField(view_name='poster-image', format='html', required=False)

    class Meta:
        model = Poster
        fields = ('url', 'id', 'title', 'image', 'image_url', 'writer', 'content', 'created', 'modified', 'end')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password')
