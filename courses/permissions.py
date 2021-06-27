from rest_framework.permissions import BasePermission


class AuthorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.author