from django.urls import path, reverse_lazy
from .views import register_request, login_request, logout_request, profile_request, ChangePasswordView, edit_profile, PasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
app_name = "accounts"   

urlpatterns = [

    path("register/", register_request, name="register"),
    path('login/',  login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('profile/', profile_request, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_reset/', PasswordResetView.as_view(), name ='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url = reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)