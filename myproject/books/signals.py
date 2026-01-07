from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book, Author

# ---------------- Book Signals ----------------
@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Book created: {instance.title}")
    else:
        print(f"[SIGNAL] Book updated: {instance.title}")

@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    print(f"[SIGNAL] Book deleted: {instance.title}")


# ---------------- Author Signals ----------------
@receiver(post_save, sender=Author)
def author_saved(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Author created: {instance.name}")
    else:
        print(f"[SIGNAL] Author updated: {instance.name}")

@receiver(post_delete, sender=Author)
def author_deleted(sender, instance, **kwargs):
    print(f"[SIGNAL] Author deleted: {instance.name}")
