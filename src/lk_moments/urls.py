from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


from registration.views import RegistrationView
from authentication.views import LoginView
from moments_feed.views import MomentsFeedView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    path('', MomentsFeedView.as_view(), name='moments_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
