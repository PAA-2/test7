from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from .models import Action
from .helpers import can_view
from .services import request_check, accept_check, reject_incomplete, reject_inadequate


@login_required
def dashboard(request):
    role = request.user.groups.first().name if request.user.groups.exists() else "U"
    kpis = {
        "total_actions": Action.objects.count(),
        "en_cours": Action.objects.filter(status="EN_COURS").count(),
        "retards": Action.objects.filter(j_delta__lt=0).count(),
        "cloturees": Action.objects.filter(status="CLOTUREE").count(),
    }
    return render(request, "paa/dashboard.html", {"role": role, "kpis": kpis})


@login_required
def actions_list(request):
    actions = Action.objects.all()
    query = request.GET.get("q")
    if query:
        actions = actions.filter(title__icontains=query)
    return render(request, "paa/actions_list.html", {"actions": actions})


@login_required
def action_detail(request, pk):
    action = get_object_or_404(Action, pk=pk)
    if not can_view(action, request.user):
        messages.error(request, "Accès refusé.")
        return redirect("dashboard")

    if request.method == "POST":
        if "request_check" in request.POST:
            request_check(action, request.user)
        elif "accept_check" in request.POST:
            accept_check(action, request.user, request.POST.get("efficacy_note", ""))
        elif "reject_incomplete" in request.POST:
            reject_incomplete(action, request.user, request.POST.get("comment", ""))
        elif "reject_inadequate" in request.POST:
            reject_inadequate(action, request.user, request.POST.get("comment", ""))
        return redirect("action_detail", pk=pk)

    return render(request, "paa/action_detail.html", {"action": action})


@login_required
def kanban_view(request):
    columns = [
        ("A_FAIRE", Action.objects.filter(status="A_FAIRE")),
        ("EN_COURS", Action.objects.filter(status="EN_COURS")),
        ("EN_TRAITEMENT", Action.objects.filter(status="EN_TRAITEMENT")),
        ("CLOTUREE", Action.objects.filter(status="CLOTUREE")),
        ("ARCHIVEE", Action.objects.filter(status="ARCHIVEE")),
    ]
    return render(request, "paa/kanban.html", {"columns": columns})


@login_required
def export_actions_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="actions.csv"'
    writer = csv.writer(response)
    writer.writerow(["Code", "Titre", "Statut", "Priorité", "Échéance", "J"])
    for a in Action.objects.all():
        writer.writerow([a.code, a.title, a.status, a.priority, a.due_date, a.j_delta])
    return response
