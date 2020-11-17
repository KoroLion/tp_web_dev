from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required


from registration.views import RegistrationView
from authentication.views import LoginView
from moments_feed.views import MomentsFeedView, MomentView, MomentsListView
from user_profile.views import Profile

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),

    path('@<str:slug>/', login_required(Profile.as_view()), name='profile'),

    path('', login_required(MomentsFeedView.as_view()), name='moments_feed'),
    path('moments/<int:pk>/', login_required(MomentView.as_view()), name='moment'),
    path('moments/best/', login_required(MomentsListView.as_view()), name='moments_best')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
