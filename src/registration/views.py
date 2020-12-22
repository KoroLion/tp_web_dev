from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, reverse, render
from django import forms

from user_profile.models import User


class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.avatar = self.cleaned_data['avatar']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegistrationView(FormView):
    template_name = "registration/registration.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        user.avatar = form.cleaned_data.get('avatar', None)
        user.save()
        login(self.request, user)
        return redirect(reverse('profile', args=(user.username,)))
