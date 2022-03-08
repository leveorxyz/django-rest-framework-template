from rest_framework.permissions import BasePermission
from user.models import User


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.ADMIN)


class OwnProfilePermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class OwnProfileViewPermission(BasePermission):
    """
    Object-level permission to only allow viewing his own profile
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
