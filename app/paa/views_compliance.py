import os
import io
import json
import zipfile
from slugify import slugify
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from paa.models import Action, Plan


User = get_user_model()


@login_required
def export_user_data(request, user_id: int):
    if (
        request.user.id != user_id
        and not request.user.groups.filter(name="SA").exists()
    ):
        return HttpResponseForbidden("Non autorisé.")
    user = get_object_or_404(User, pk=user_id)

    bundle = {
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "actions_responsable": list(
            Action.objects.filter(responsables=user).values(
                "id", "code", "title", "status", "due_date"
            )
        ),
        "actions_creees": list(
            Action.objects.filter(created_by=user).values(
                "id", "code", "title", "status", "due_date"
            )
        ),
        "plans_possedes": list(
            Plan.objects.filter(owner=user).values("id", "code", "name", "mode")
        ),
    }

    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    base = f"{slugify(user.username)}_export.json"
    tmp_json = io.BytesIO(
        json.dumps(bundle, default=str, ensure_ascii=False, indent=2).encode("utf-8")
    )

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(base, tmp_json.getvalue())
    zip_buf.seek(0)
    filename = f"{slugify(user.username)}_export.zip"
    return FileResponse(zip_buf, as_attachment=True, filename=filename)
