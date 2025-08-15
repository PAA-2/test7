import uuid
from datetime import date

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .helpers import can_transition
from .models import Action


def generate_action_code() -> str:
    """Génère un code unique lisible pour une action (Axxxx)."""
    return f"A{uuid.uuid4().hex[:6].upper()}"


def compute_j_delta(action: Action) -> int:
    """Calcule le delta J selon les règles métier."""
    if action.status != "CLOTUREE" and action.due_date:
        return (action.due_date - date.today()).days
    if action.status == "CLOTUREE" and action.due_date and action.done_at:
        return (action.done_at - action.due_date).days
    return 0


@transaction.atomic
def request_check(action: Action, actor):
    """Demande de check/clôture."""
    if not can_transition(action, actor):
        raise PermissionDenied("Pas autorisé à demander un check.")
    action.status = "EN_TRAITEMENT"
    action.save()
    return action


@transaction.atomic
def accept_check(action: Action, actor, efficacy_note: str):
    """Accepte une clôture après évaluation efficacité."""
    if not can_transition(action, actor):
        raise PermissionDenied("Pas autorisé à clôturer.")
    if not efficacy_note.strip():
        raise ValidationError("L'évaluation d’efficacité est obligatoire.")
    action.status = "CLOTUREE"
    action.efficacy_note = efficacy_note
    action.done_at = date.today()
    action.j_delta = compute_j_delta(action)
    action.save()
    return action


@transaction.atomic
def reject_incomplete(action: Action, actor, comment: str):
    """Rejet pour incomplet : retour en cours."""
    if not can_transition(action, actor):
        raise PermissionDenied("Pas autorisé à rejeter.")
    action.status = "EN_COURS"
    action.efficacy_note = comment
    action.save()
    return action


@transaction.atomic
def reject_inadequate(action: Action, actor, comment: str):
    """Rejet pour inadéquat : crée une nouvelle action liée."""
    if not can_transition(action, actor):
        raise PermissionDenied("Pas autorisé à rejeter.")
    new_action = Action.objects.create(
        code=generate_action_code(),
        title=f"[Relance] {action.title}",
        description=comment,
        created_by=actor,
    )
    action.status = "ARCHIVEE"
    action.action_parent = new_action
    action.save()
    return action, new_action
