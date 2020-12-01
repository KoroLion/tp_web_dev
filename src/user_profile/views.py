from django.views.generic import DetailView, FormView, UpdateView
from django.forms import ModelForm

from user_profile.models import User


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=True)


class Profile(DetailView):
    model = User
    template_name = 'user_profile/profile.html'
    slug_field = 'username'


class ProfileEdit(UpdateView):
    model = User
    template_name = 'user_profile/profile_edit.html'
    slug_field = 'username'
    form_class = UserEditForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()
