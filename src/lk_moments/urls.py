from django.contrib import admin
from django.urls import path

from registration.views import RegistrationView
from authentication.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
]
