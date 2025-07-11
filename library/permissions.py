from rest_framework.permissions import BasePermission, SAFE_METHODS

class Amin_Other(BasePermission):
    def giving_per(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
