from django.shortcuts import render

# Create your views here.
from django.urls import path
from .views import register_request, login_request, logout_request, profile_request, ChangePasswordView, edit_profile
from django.conf import settings
from django.conf.urls.static import static
app_name = "main"   


urlpatterns = [

    path("register/", register_request, name="register"),
    path('login/',  login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('profile/', profile_request, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/password-change/', ChangePasswordView.as_view(), name='password_change')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)