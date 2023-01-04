from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class AuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.method in SAFE_METHODS:
            return True
            
        if obj.user == request.user:
            return True

        raise PermissionDenied
