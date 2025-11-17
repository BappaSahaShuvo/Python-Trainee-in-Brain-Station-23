# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Signup
    path('signup/', views.signup_view, name='signup'),
    path('verify-signup-otp/', views.verify_signup_otp, name='verify_signup_otp'),
    path('resend-signup-otp/', views.resend_signup_otp, name='resend_signup_otp'),

    # Login
    path('login/', views.login_view, name='login'),
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),
    path('resend-login-otp/', views.resend_login_otp, name='resend_login_otp'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard / profile
    path('dashboard/', views.profile, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # Password reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),

    # Email change
    path('email-change/', views.email_change_request, name='email_change_request'),
    path('email-change/verify/', views.email_change_verify, name='email_change_verify'),

    # Admin
    path('admin-notifications/', views.admin_notifications, name='admin_notifications'),
]
