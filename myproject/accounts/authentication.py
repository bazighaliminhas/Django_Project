from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import AuthToken

class AuthUserWrapper:
    """Wrapper to add is_authenticated property for DRF."""
    def __init__(self, user):
        self.user = user
        self.is_authenticated = True  # ✅ This is what DRF checks

    def __getattr__(self, name):
        return getattr(self.user, name)


class CustomTokenAuthentication(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed('Invalid token header')

        token_key = parts[1]

        try:
            token_obj = AuthToken.objects.get(token=token_key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (AuthUserWrapper(token_obj.user), None)  # wrap user
