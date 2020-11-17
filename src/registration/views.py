from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, reverse, render
from django import forms

from user_profile.models import User


class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegistrationView(TemplateView):
    template_name = "registration/registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomUserCreationForm()
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            user.avatar = form.cleaned_data.get('avatar', None)
            user.save()
            login(request, user)
            return redirect(reverse('profile', args=(user.username,)))

        return render(request, self.template_name, {'form': form})
