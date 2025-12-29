from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # Home page with Get Started
    path('landing/', views.landing, name='landing'),  # After Get Started page
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

]
