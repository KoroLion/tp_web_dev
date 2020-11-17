from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


class LoginView(TemplateView):
    _form_class = AuthenticationForm
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
        form = self._form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', reverse('moments_feed'))
            return redirect(next_url)

        return render(request, self.template_name, {'form': form})
