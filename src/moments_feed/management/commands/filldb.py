import random
from faker import Faker
import pytz
import datetime

from django.core.management.base import BaseCommand

from user_profile.models import User
from moments_feed.models import Moment, Like

faker = Faker()
default_images = [
    'Chrysanthemum.jpg', 'Desert.jpg', 'Hydrangeas.jpg',
    'Jellyfish.jpg', 'Koala.jpg', 'Lighthouse.jpg',
    'Penguins.jpg', 'Tulips.jpg'
]



class Command(BaseCommand):
    _uid = 1

    @staticmethod
    def __random_dt():
        date = faker.date_object()
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        dt = pytz.timezone('UTC').localize(dt, is_dst=None)
        return dt

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10)
        parser.add_argument('--moments', type=int, default=100)
        parser.add_argument('--likes', type=int, default=500)

    def create_users(self, amount):
        users_to_create = amount - User.objects.count()
        users = []
        for i in range(0, users_to_create):
            suid = str(self._uid)
            users.append(User(
                username=faker.user_name() + suid,
                email=faker.email() + suid)
            )
            self._uid += 1
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('Created {} users'.format(users_to_create)))

    def create_moments(self, amount):
        user_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        moments_to_create = amount - Moment.objects.count()
        moments = []
        for i in range(0, moments_to_create):
            moment = Moment(
                author_id=random.choice(user_ids),
                description=faker.text().split('\n')[0][0:128],
                created_date=self.__random_dt()
            )
            moment.image = 'default/' + random.choice(default_images)
            moments.append(moment)

        Moment.objects.bulk_create(moments)

        self.stdout.write(self.style.SUCCESS('Created {} moments'.format(moments_to_create)))

    def create_likes(self, amount):
        user_ids = list(User.objects.values_list(
            'id', flat=True
        ))
        moment_ids = list(Moment.objects.values_list(
            'id', flat=True
        ))

        likes_to_create = amount - Like.objects.count()
        likes = []
        for i in range(0, likes_to_create):
            likes.append(Like(
                author_id=random.choice(user_ids),
                moment_id=random.choice(moment_ids),
                created_date=self.__random_dt()
            ))
        Like.objects.bulk_create(likes)

        self.stdout.write(self.style.SUCCESS('Created {} likes'.format(likes_to_create)))

    def handle(self, *args, **options):
        self.create_users(options['users'])
        self.create_moments(options['moments'])
        self.create_likes(options['likes'])
