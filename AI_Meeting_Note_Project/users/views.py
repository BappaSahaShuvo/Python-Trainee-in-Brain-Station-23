from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import CustomUser, EmailOTP
from .forms import SignupForm, LoginForm
from .utils import send_otp_email
from django.conf import settings


def home(request):
    return render(request, 'home.html')


def landing(request):
    return render(request, 'landing.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('signup')

            user = CustomUser.objects.create_user(
                email=email,
                full_name=form.cleaned_data['full_name'],
                password=form.cleaned_data['password']
            )
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.age = form.cleaned_data['age']
            user.phone = form.cleaned_data['phone']
            user.is_active = False
            user.save()

            send_otp_email(user, 'signup')
            request.session['otp_user'] = user.email
            request.session['otp_purpose'] = 'signup'
            return redirect('verify_otp')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                send_otp_email(user, 'login')
                request.session['otp_user'] = user.email
                request.session['otp_purpose'] = 'login'
                return redirect('verify_otp')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def verify_otp(request):
    email = request.session.get('otp_user')
    purpose = request.session.get('otp_purpose')

    if not email or not purpose:
        return redirect('login')

    try:
        user = CustomUser.objects.get(email=email)
        otp_obj = EmailOTP.objects.filter(
            user=user, purpose=purpose
        ).latest('created_at')
    except:
        messages.error(request, "OTP not found. Please resend.")
        return redirect('login')

    otp_valid_seconds = getattr(settings, 'OTP_VALID_SECONDS', 60)
    remaining = max(0, int((otp_obj.expires_at - timezone.now()).total_seconds()))

    if request.method == 'POST':
        if 'resend' in request.POST:
            send_otp_email(user, purpose)
            return redirect('verify_otp')

        entered_otp = request.POST.get('otp')

        if otp_obj.is_expired():
            messages.error(request, "OTP expired")
        elif otp_obj.otp != entered_otp:
            messages.error(request, "Wrong OTP")
        else:
            otp_obj.is_verified = True
            otp_obj.save()

            if purpose == 'signup':
                user.is_active = True
                user.save()

            login(request, user)
            return redirect('dashboard')

    return render(request, 'otp_verify.html', {
        'remaining': remaining,
        'otp_valid_seconds': otp_valid_seconds
    })


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        user.full_name = request.POST.get("full_name")
        user.phone = request.POST.get("phone")
        user.date_of_birth = request.POST.get("date_of_birth") or None
        user.age = request.POST.get("age") or None

        # ✅ HANDLE PROFILE IMAGE UPLOAD
        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES["profile_image"]

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')  # ✅ redirect after POST

    return render(request, "profile.html")
