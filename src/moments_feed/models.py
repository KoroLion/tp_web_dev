import os
from uuid import uuid1

from django.db import models
from django.dispatch import receiver

from utils.img_tools import compress_image
from user_profile.models import User


def get_moment_image_path(instance, filename):
    return 'moments/user_{}/{}.jpg'.format(instance.author.id, uuid1())


class Moment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_moment_image_path)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image.path, 600, 600)


@receiver(models.signals.post_delete, sender=Moment)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
