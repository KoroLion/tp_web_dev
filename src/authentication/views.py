from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = "authentication/login.html"

    def get_success_url(self):
        return reverse('moments_feed')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
