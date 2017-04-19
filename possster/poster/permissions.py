from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsWriterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.writer == request.user


class IsUserSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsUserSelfOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user and request.user.is_staff


class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous()
