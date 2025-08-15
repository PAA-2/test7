from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class PlaceholderSSOBackend:
    """Backend SSO désactivable. Si SSO_ENABLED=false => ne fait rien."""

    def authenticate(self, request, **kwargs):
        if not getattr(settings, "SSO_ENABLED", False):
            return None
        remote = request.META.get("HTTP_X_REMOTE_USER")
        if not remote:
            return None
        user, _ = User.objects.get_or_create(
            username=remote, defaults={"email": f"{remote}@sso.local"}
        )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
