from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Action
from .services import generate_action_code, compute_j_delta


@receiver(pre_save, sender=Action)
def auto_generate_code_and_j(sender, instance, **kwargs):
    if not instance.code:
        instance.code = generate_action_code()
    instance.j_delta = compute_j_delta(instance)
