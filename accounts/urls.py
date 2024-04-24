from django.urls import path
from accounts.views import *
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_auth, name="login"),
    path('user/<int:id>', profile, name="profile"),
    path('forgot-password/', ForgetPassword.as_view(), name="forgot-password"),
    # path('success-password-request', success_password_request, name="success-password-request"),
    path('log-out', LogoutView.as_view(), name='log-out'),
    path('edit-profile/<int:pk>', EditProfile.as_view(), name="edit-profile"),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(), name = 'password-reset-confirm'),
]
