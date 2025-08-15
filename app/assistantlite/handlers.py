from datetime import date
from django.contrib.auth import get_user_model
from django.db import transaction
from paa.models import Action, Plan
from paa.services import request_check
from paa.importer import import_plan_from_excel
from paa.models_import import ImportProfile
from paa.helpers import can_edit

User = get_user_model()


@transaction.atomic
def create_action_handler(request, groups):
    title = groups.get("title", "").strip()
    if not title:
        return {"ok": False, "msg": "Titre manquant."}
    plan = Plan.objects.filter(owner=request.user).first()
    a = Action.objects.create(title=title, created_by=request.user)
    if plan:
        from paa.models import ActionPlan

        ActionPlan.objects.get_or_create(action=a, plan=plan)
    return {"ok": True, "action_id": str(a.id), "code": a.code}


def request_check_handler(request, groups):
    code = groups.get("code", "").strip().upper()
    try:
        a = Action.objects.get(code=code)
    except Action.DoesNotExist:
        return {"ok": False, "msg": "Action introuvable."}
    if not can_edit(a, request.user):
        return {"ok": False, "msg": "Droits insuffisants."}
    request_check(a, request.user)
    return {"ok": True, "status": a.status}


def set_due_handler(request, groups):
    code = groups.get("code", "").strip().upper()
    days = int(groups.get("days", "0"))
    try:
        a = Action.objects.get(code=code)
    except Action.DoesNotExist:
        return {"ok": False, "msg": "Action introuvable."}
    if not can_edit(a, request.user):
        return {"ok": False, "msg": "Droits insuffisants."}
    from datetime import timedelta

    a.due_date = date.today() + timedelta(days=days)
    a.save(update_fields=["due_date"])
    return {"ok": True, "due_date": str(a.due_date)}


def sync_plan_handler(request, groups):
    plan_code = groups.get("plan", "").strip()
    try:
        plan = Plan.objects.get(code=plan_code)
    except Plan.DoesNotExist:
        return {"ok": False, "msg": "Plan introuvable."}
    profile = ImportProfile.objects.first()
    file_path = f"/media/{plan.code}.xlsx"
    report = import_plan_from_excel(plan, file_path, profile)
    return {
        "ok": True,
        "created": report.created_count,
        "updated": report.updated_count,
        "skipped": report.skipped_count,
    }


def export_csv_handler(request, groups):
    return {"ok": True, "redirect": "/export/actions/"}
