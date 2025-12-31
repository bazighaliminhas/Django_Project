from rest_framework.permissions import BasePermission

class IsEmailAdmin(BasePermission):
    """
    Allow access only to admin email
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.email == "bazighaliminhas1@gmail.com"
