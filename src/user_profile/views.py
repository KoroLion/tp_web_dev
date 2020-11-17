from django.views.generic import TemplateView


class Profile(TemplateView):
    template_name = 'user_profile/profile.html'
