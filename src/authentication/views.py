from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


class LoginView(TemplateView):
    _form_class = AuthenticationForm
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
        form = self._form_class(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect(reverse('moments_feed'))

        return render(request, self.template_name, {'form': form})
