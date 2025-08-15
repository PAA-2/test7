from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from paa.models_adminpanel import SystemSettings
from .intents import INTENTS
from .models import AssistantLog, FAQ


def _assistant_enabled() -> bool:
    s, _ = SystemSettings.objects.get_or_create(pk=1)
    return bool(s.feature_flags.get("assistant_enabled", True))


@login_required
@require_POST
def trigger(request):
    if not _assistant_enabled():
        return JsonResponse({"ok": False, "msg": "Assistant désactivé."}, status=403)
    text = (request.POST.get("q") or "").strip()
    if not text:
        return JsonResponse({"ok": False, "msg": "Commande vide."}, status=400)

    for rule in INTENTS:
        m = rule.pattern.match(text)
        if m:
            groups = m.groupdict()
            result = rule.handler(request, groups)
            AssistantLog.objects.create(
                user=request.user, intent=rule.name, payload=groups, result=result
            )
            return JsonResponse({"intent": rule.name, **result})
    AssistantLog.objects.create(
        user=request.user, intent="unmatched", payload={"q": text}, result={"ok": False}
    )
    return JsonResponse({"ok": False, "msg": "Commande non reconnue."}, status=400)


@login_required
def faq_list(request):
    q = (request.GET.get("q") or "").strip().lower()
    items = FAQ.objects.all()
    if q:
        items = items.filter(question__icontains=q)
    return render(request, "assistantlite/faq.html", {"items": items, "q": q})


@login_required
def logs(request):
    items = AssistantLog.objects.select_related("user")[:200]
    return render(request, "assistantlite/logs.html", {"items": items})
