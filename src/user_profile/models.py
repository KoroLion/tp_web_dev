from uuid import uuid1
import os

from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.img_tools import compress_image


def get_avatar_image_path(instance, filename):
    return 'avatars/user_{}.jpg'.format(instance.id, uuid1())


class User(AbstractUser):
    avatar = models.ImageField(upload_to=get_avatar_image_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            compress_image(self.avatar.path, 256, 256)


@receiver(models.signals.post_delete, sender=User)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
