from django.views.generic import DetailView

from user_profile.models import User


class Profile(DetailView):
    model = User
    template_name = 'user_profile/profile.html'
    slug_field = 'username'
