from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category

# ---------------- Category Signals ----------------
@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Category created: {instance.name}")
    else:
        print(f"[SIGNAL] Category updated: {instance.name}")


@receiver(post_delete, sender=Category)
def category_deleted(sender, instance, **kwargs):
    print(f"[SIGNAL] Category deleted: {instance.name}")
