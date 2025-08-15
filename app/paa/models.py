import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Plan(models.Model):
    MODE_CHOICES = [
        ("EXCEL", "Excel Externe"),
        ("INTERNE", "Mode Interne"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nom du plan", max_length=255)
    code = models.CharField("Code plan", max_length=50, unique=True)
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="plans_possedes"
    )
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default="EXCEL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} — {self.name}"


class Action(models.Model):
    STATUS_CHOICES = [
        ("A_FAIRE", "À faire"),
        ("EN_COURS", "En cours"),
        ("EN_TRAITEMENT", "En traitement"),
        ("CLOTUREE", "Clôturée"),
        ("ARCHIVEE", "Archivée"),
    ]
    PRIORITY_CHOICES = [
        ("LOW", "Basse"),
        ("MED", "Moyenne"),
        ("HIGH", "Haute"),
        ("CRIT", "Critique"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Code action", max_length=50, unique=True)
    title = models.CharField("Titre", max_length=255)
    description = models.TextField("Description", blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MED")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="A_FAIRE")
    due_date = models.DateField("Échéance", null=True, blank=True)
    done_at = models.DateField("Date réalisation", null=True, blank=True)
    efficacy_note = models.TextField("Évaluation efficacité", blank=True)
    j_delta = models.IntegerField("Jours de delta", default=0, editable=False)
    action_parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actions_liees",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="actions_creees"
    )
    responsables = models.ManyToManyField(
        User, related_name="actions_responsables", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} — {self.title}"


class ActionPlan(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("action", "plan")

    def __str__(self):
        return f"{self.action.code} ↔ {self.plan.code}"
