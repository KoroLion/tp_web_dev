from django.contrib import admin
from django.urls import path

from registration.views import RegistrationView
from authentication.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('signup/', RegistrationView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
]
