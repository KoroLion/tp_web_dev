from uuid import uuid1
import os

from django.utils import timezone
from datetime import timedelta

from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser

# from moments_feed.models import Like
from utils.img_tools import compress_image


def get_avatar_image_path(instance, filename):
    return 'avatars/user_{}.jpg'.format(instance.id, uuid1())


class User(AbstractUser):
    avatar = models.ImageField(upload_to=get_avatar_image_path, null=True, blank=True)

    # def get_latest_likes(self):
    #     start_date = timezone.now() - timedelta(days=5)
    #     end_date = timezone.now()
    #     likes = Like.objects.filter(created_date__range=[start_date, end_date])
    #     return likes

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            compress_image(self.avatar.path, 256, 256, False)


@receiver(models.signals.post_delete, sender=User)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_avatar = User.objects.get(pk=instance.pk).avatar
    except User.DoesNotExist:
        return False

    if instance.avatar != old_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
