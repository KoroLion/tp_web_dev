from django.urls import path

from moments_feed import views

app_name = "lk_profile"

# views related to personal profile only
urlpatterns = [
    path('', views.MomentsFeedView, name='moments_feed'),
]
