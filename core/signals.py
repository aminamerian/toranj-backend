from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category


@receiver(post_save, sender=Category)
def update_is_leaf_field(sender, instance, **kwargs):
    """
    The signal changes is_leaf field of the parent category to False if it is True.
    It means that the category has a child now and is not a leaf anymore.
    """
    parent = instance.parent
    if parent is not None:
        if parent.is_leaf:
            parent.is_leaf = False
            parent.save()
