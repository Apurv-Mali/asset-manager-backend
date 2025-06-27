from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Asset,Notification
from django.contrib.auth import get_user_model

@receiver(post_save,sender=Asset)
def asset_created(sender,instance,created,**kwargs):
    if created:
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)

        for superuser in superusers:
            recipent = superuser
            message = f'New Asset {instance.name} was added Sucessfully'
            Notification.objects.create(recipient=recipent,message=message)