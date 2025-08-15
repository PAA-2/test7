from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import connection
from .models import Action
from .services import generate_action_code, compute_j_delta
from .models_attachments import Attachment
from .ocr import extract_text_from_file, sha256_file


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
