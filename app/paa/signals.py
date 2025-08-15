from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.db import connection
from django.forms.models import model_to_dict
from .models import Action, Plan
from .services import generate_action_code, compute_j_delta
from .models_attachments import Attachment
from .ocr import extract_text_from_file, sha256_file
from .audit import write_audit


@receiver(pre_save, sender=Action)
def auto_generate_code_and_j(sender, instance, **kwargs):
    if not instance.code:
        instance.code = generate_action_code()
    instance.j_delta = compute_j_delta(instance)


@receiver(post_save, sender=Attachment)
def ocr_and_index_attachment(sender, instance: Attachment, created, **kwargs):
    if created and instance.file:
        instance.size = instance.file.size or 0
        instance.mime = instance.mime or (
            instance.file.file.content_type
            if hasattr(instance.file.file, "content_type")
            else ""
        )
        instance.sha256 = sha256_file(instance.file)
        instance.ocr_text = extract_text_from_file(instance.file)
        instance.save(update_fields=["size", "mime", "sha256", "ocr_text"])
    with connection.cursor() as cur:
        cur.execute(
            "SELECT paa_update_action_search_vector(%s)", [str(instance.action_id)]
        )


@receiver(pre_save, sender=Action)
def audit_action_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            before = model_to_dict(Action.objects.get(pk=instance.pk))
        except Action.DoesNotExist:
            before = {}
        instance._audit_before = before


@receiver(post_save, sender=Action)
def audit_action_post_save(sender, instance, created, **kwargs):
    before = getattr(instance, "_audit_before", {}) if not created else {}
    after = model_to_dict(instance)
    write_audit(
        instance, "created" if created else "updated", before=before, after=after
    )


@receiver(pre_delete, sender=Action)
def audit_action_delete(sender, instance, **kwargs):
    write_audit(instance, "deleted", before=model_to_dict(instance), after={})


@receiver(pre_save, sender=Plan)
def audit_plan_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            before = model_to_dict(Plan.objects.get(pk=instance.pk))
        except Plan.DoesNotExist:
            before = {}
        instance._audit_before = before


@receiver(post_save, sender=Plan)
def audit_plan_post_save(sender, instance, created, **kwargs):
    before = getattr(instance, "_audit_before", {}) if not created else {}
    after = model_to_dict(instance)
    write_audit(
        instance, "created" if created else "updated", before=before, after=after
    )
