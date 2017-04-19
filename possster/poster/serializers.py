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
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Not match password")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'password_confirm', 'email')
