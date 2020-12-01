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
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=get_moment_image_path)
    created_date = models.DateTimeField()

    def __str__(self):
        return 'Moment {}'.format(self.pk)

    def get_comments_descending(self):
        return self.comment_set.all().order_by('-id')

    def save(self, *args, **kwargs):
        if self.image:
            compress_image(self.image.path, 600, 600)


@receiver(models.signals.post_delete, sender=Moment)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Comment(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=512)
    created_date = models.DateTimeField()


class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    subscribed_date = models.DateTimeField()


class Like(models.Model):
    # change to django mechanism for multiple tables
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField()


class Tag(models.Model):
    moment = models.ManyToManyField(Moment)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
