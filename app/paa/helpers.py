"""Helpers de permissions basées sur les rôles."""

from django.contrib.auth.models import Group  # noqa: F401

from .models import Action, Plan

ROLE_SUPER_ADMIN = "SA"
ROLE_PILOTE_PROCESSUS = "PP"
ROLE_PILOTE = "P"
ROLE_UTILISATEUR = "U"


def get_user_role(user):
    """Retourne le rôle principal de l’utilisateur."""
    for role in [
        ROLE_SUPER_ADMIN,
        ROLE_PILOTE_PROCESSUS,
        ROLE_PILOTE,
        ROLE_UTILISATEUR,
    ]:
        if user.groups.filter(name=role).exists():
            return role
    return ROLE_UTILISATEUR


def can_view(obj: Plan | Action, user) -> bool:
    """Lecture selon rôle."""
    role = get_user_role(user)
    if role in [ROLE_SUPER_ADMIN, ROLE_PILOTE_PROCESSUS]:
        return True
    if role == ROLE_PILOTE:
        if isinstance(obj, Plan):
            return obj.owner == user
        if isinstance(obj, Action) and hasattr(obj, "plan"):
            return obj.plan.owner == user
    if role == ROLE_UTILISATEUR and isinstance(obj, Action):
        return user in obj.responsables.all()
    return False


def can_edit(obj: Plan | Action, user) -> bool:
    """Édition selon rôle."""
    role = get_user_role(user)
    if role in [ROLE_SUPER_ADMIN, ROLE_PILOTE_PROCESSUS]:
        return True
    if role == ROLE_PILOTE:
        if isinstance(obj, Plan):
            return obj.owner == user
        if isinstance(obj, Action) and hasattr(obj, "plan"):
            return obj.plan.owner == user
    return False


def can_transition(obj: Plan | Action, user) -> bool:
    """Transitions PDCA selon rôle."""
    role = get_user_role(user)
    if role in [ROLE_SUPER_ADMIN, ROLE_PILOTE_PROCESSUS]:
        return True
    if role == ROLE_PILOTE:
        if isinstance(obj, Plan):
            return obj.owner == user
        if isinstance(obj, Action) and hasattr(obj, "plan"):
            return obj.plan.owner == user
    return False
