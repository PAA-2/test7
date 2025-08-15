import json
from django.core.serializers.json import DjangoJSONEncoder
from .security import get_current_user
from .models_audit import AuditLog

SENSITIVE_FIELDS = {"password", "secret", "token", "key", "FERNET_KEY"}


def _clean(data):
    return json.loads(
        json.dumps(
            {
                k: ("***" if k.lower() in SENSITIVE_FIELDS else v)
                for k, v in (data or {}).items()
            },
            cls=DjangoJSONEncoder,
        )
    )


def write_audit(instance, verb: str, before=None, after=None, request=None):
    user = get_current_user()
    username = getattr(user, "username", "") if user else ""
    ip = request.META.get("REMOTE_ADDR") if request else ""
    ua = request.META.get("HTTP_USER_AGENT") if request else ""
    AuditLog.objects.create(
        actor=username,
        verb=verb,
        obj_type=instance.__class__.__name__,
        obj_id=str(getattr(instance, "pk", "")),
        before=_clean(before),
        after=_clean(after),
        ip=ip or "",
        user_agent=ua or "",
    )
