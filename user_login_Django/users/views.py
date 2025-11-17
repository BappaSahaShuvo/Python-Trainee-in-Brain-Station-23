# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.utils import timezone

from .models import CustomUser, OTP, AdminNotification
from .forms import SignupForm, LoginForm, OTPForm, PasswordResetRequestForm, PasswordResetConfirmForm, EmailChangeRequestForm

# -----------------------
# helper: send OTP email
# -----------------------
def _send_email_otp(email, otp_code, subject="Your OTP Verification Code"):
    body = f"Your OTP code is: {otp_code}\nThis code is valid for {getattr(settings,'OTP_VALID_SECONDS',60)} seconds.\n\nIf you did not request this, ignore."
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)


# -----------------------
# Home
# -----------------------
def home(request):
    return render(request, "users/home.html")


# -----------------------
# SIGNUP -> OTP
# -----------------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = CustomUser.objects.create_user(
                email=data['email'].lower(),
                password=data['password'],
                name=data.get('name',''),
                is_active=False
            )
            # save profile fields on user model
            user.address = data.get('address','')
            user.phone = data.get('phone','')
            user.nid_number = data.get('nid_number','')
            user.age = data.get('age')
            user.date_of_birth = data.get('date_of_birth')
            user.gender = data.get('gender','')
            if data.get('picture'):
                user.picture = data.get('picture')
            user.save()

            # create OTP and send
            otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
            _send_email_otp(user.email, otp.code, subject="Signup OTP")

            # session
            request.session['pending_signup_user_id'] = user.id
            request.session['pending_signup_otp_uuid'] = str(otp.uuid)

            return redirect('verify_signup_otp')
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {'form': form})


def verify_signup_otp(request):
    user_id = request.session.get('pending_signup_user_id')
    otp_uuid = request.session.get('pending_signup_otp_uuid')
    if not user_id or not otp_uuid:
        messages.error(request, "No pending signup found. Please signup again.")
        return redirect('signup')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found. Please signup again.")
        return redirect('signup')

    try:
        otp = OTP.objects.get(uuid=otp_uuid, user=user, is_used=False)
    except OTP.DoesNotExist:
        messages.error(request, "OTP not found or already used.")
        return redirect('signup')

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data['otp'].strip()
            now = timezone.now()
            if now > otp.expires_at:
                messages.error(request, "OTP expired. Please resend.")
                return redirect('resend_signup_otp')
            if entered != otp.code:
                messages.error(request, "Wrong OTP. please write the correct OTP.")
                return redirect('verify_signup_otp')

            # success
            otp.mark_used()
            user.is_active = True
            user.save()

            AdminNotification.objects.create(message=f'{user.get_full_name()} , {user.email} signup')

            # cleanup session
            request.session.pop('pending_signup_user_id', None)
            request.session.pop('pending_signup_otp_uuid', None)

            messages.success(request, "Signup successful. Please login.")
            return redirect('login')
    else:
        form = OTPForm()

    remaining = otp.time_left()
    return render(request, "users/verify_signup_otp.html", {'form': form, 'remaining': remaining})


def resend_signup_otp(request):
    user_id = request.session.get('pending_signup_user_id')
    otp_uuid = request.session.get('pending_signup_otp_uuid')
    if not user_id or not otp_uuid:
        messages.error(request, "No signup OTP process found.")
        return redirect('signup')

    user = get_object_or_404(CustomUser, id=user_id)
    # allow only after previous expired (optional)
    # delete previous OTPs for this user for clarity
    OTP.objects.filter(user=user, is_used=False).delete()
    new_otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
    _send_email_otp(user.email, new_otp.code, subject="Signup OTP (Resent)")
    request.session['pending_signup_otp_uuid'] = str(new_otp.uuid)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_signup_otp')


# -----------------------
# LOGIN -> OTP
# -----------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is None:
                messages.error(request, "Invalid credentials or account not found.")
                return redirect('login')
            if not user.is_active:
                messages.error(request, "Account inactive. Complete signup verification.")
                return redirect('login')

            # create OTP and send (login)
            otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
            _send_email_otp(user.email, otp.code, subject="Login OTP")

            request.session['pending_login_user_id'] = user.id
            request.session['pending_login_otp_uuid'] = str(otp.uuid)
            return redirect('verify_login_otp')
    else:
        form = LoginForm()
    return render(request, "users/login.html", {'form': form})


def verify_login_otp(request):
    user_id = request.session.get('pending_login_user_id')
    otp_uuid = request.session.get('pending_login_otp_uuid')
    if not user_id or not otp_uuid:
        messages.error(request, "No login process in progress.")
        return redirect('login')

    user = get_object_or_404(CustomUser, id=user_id)
    otp = get_object_or_404(OTP, uuid=otp_uuid, user=user, is_used=False)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data['otp'].strip()
            now = timezone.now()
            if now > otp.expires_at:
                messages.error(request, "OTP expired. Please resend.")
                return redirect('resend_login_otp')
            if entered != otp.code:
                messages.error(request, "Wrong OTP. please write the correct OTP.")
                return redirect('verify_login_otp')

            otp.mark_used()
            auth_login(request, user)
            AdminNotification.objects.create(message=f'{user.get_full_name()} , {user.email} Login')

            request.session.pop('pending_login_user_id', None)
            request.session.pop('pending_login_otp_uuid', None)

            messages.success(request, "Login successful.")
            return redirect('dashboard')
    else:
        form = OTPForm()

    remaining = otp.time_left()
    return render(request, "users/verify_login_otp.html", {'form': form, 'remaining': remaining})


def resend_login_otp(request):
    user_id = request.session.get('pending_login_user_id')
    otp_uuid = request.session.get('pending_login_otp_uuid')
    if not user_id or not otp_uuid:
        messages.error(request, "No login OTP process found.")
        return redirect('login')

    user = get_object_or_404(CustomUser, id=user_id)
    OTP.objects.filter(user=user, is_used=False).delete()
    new_otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
    _send_email_otp(user.email, new_otp.code, subject="Login OTP (Resent)")

    request.session['pending_login_otp_uuid'] = str(new_otp.uuid)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_login_otp')


# -----------------------
# PASSWORD RESET via OTP
# -----------------------
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            try:
                user = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "No account with that email.")
                return redirect('password_reset_request')

            OTP.objects.filter(user=user, is_used=False).delete()
            otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
            _send_email_otp(user.email, otp.code, subject="Password Reset OTP")

            request.session['password_reset_user_id'] = user.id
            request.session['password_reset_otp_uuid'] = str(otp.uuid)
            return redirect('password_reset_confirm')
    else:
        form = PasswordResetRequestForm()
    return render(request, "users/password_reset_request.html", {'form': form})


def password_reset_confirm(request):
    user_id = request.session.get('password_reset_user_id')
    otp_uuid = request.session.get('password_reset_otp_uuid')
    if not user_id or not otp_uuid:
        messages.error(request, "No password reset in progress.")
        return redirect('password_reset_request')

    user = get_object_or_404(CustomUser, id=user_id)
    otp = get_object_or_404(OTP, uuid=otp_uuid, user=user, is_used=False)

    if request.method == "POST":
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data['otp'].strip()
            new_password = form.cleaned_data['new_password']
            new_password2 = form.cleaned_data['new_password2']
            if new_password != new_password2:
                messages.error(request, "Passwords do not match.")
                return redirect('password_reset_confirm')

            now = timezone.now()
            if now > otp.expires_at:
                messages.error(request, "OTP expired. Please request again.")
                return redirect('password_reset_request')
            if entered != otp.code:
                messages.error(request, "Wrong OTP.")
                return redirect('password_reset_confirm')

            otp.mark_used()
            user.set_password(new_password)
            user.save()
            request.session.pop('password_reset_user_id', None)
            request.session.pop('password_reset_otp_uuid', None)
            messages.success(request, "Password reset successful. Please login.")
            return redirect('login')
    else:
        form = PasswordResetConfirmForm()
    remaining = otp.time_left()
    return render(request, "users/password_reset_confirm.html", {'form': form, 'remaining': remaining})


# -----------------------
# EMAIL CHANGE (request -> verify)
# -----------------------
@login_required
def email_change_request(request):
    if request.method == "POST":
        form = EmailChangeRequestForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email'].lower()
            if CustomUser.objects.filter(email__iexact=new_email).exists():
                messages.error(request, "This email is already in use.")
                return redirect('email_change_request')
            user = request.user
            OTP.objects.filter(user=user, is_used=False).delete()
            otp = OTP.create_otp(user, valid_seconds=getattr(settings, "OTP_VALID_SECONDS", 60))
            _send_email_otp(new_email, otp.code, subject="Email Change OTP")
            request.session['email_change_new_email'] = new_email
            request.session['email_change_otp_uuid'] = str(otp.uuid)
            return redirect('email_change_verify')
    else:
        form = EmailChangeRequestForm()
    return render(request, "users/email_change_request.html", {'form': form})


@login_required
def email_change_verify(request):
    new_email = request.session.get('email_change_new_email')
    otp_uuid = request.session.get('email_change_otp_uuid')
    if not new_email or not otp_uuid:
        messages.error(request, "No email change request found.")
        return redirect('profile')

    user = request.user
    otp = get_object_or_404(OTP, uuid=otp_uuid, user=user, is_used=False)
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data['otp'].strip()
            now = timezone.now()
            if now > otp.expires_at:
                messages.error(request, "OTP expired.")
                return redirect('email_change_request')
            if entered != otp.code:
                messages.error(request, "Wrong OTP.")
                return redirect('email_change_verify')
            otp.mark_used()
            user.email = new_email
            user.save()
            request.session.pop('email_change_new_email', None)
            request.session.pop('email_change_otp_uuid', None)
            messages.success(request, "Email changed successfully.")
            return redirect('profile')
    else:
        form = OTPForm()
    remaining = otp.time_left()
    return render(request, "users/email_change_verify.html", {'form': form, 'remaining': remaining})


# -----------------------
# PROFILE / LOGOUT / ADMIN NOTIFS
# -----------------------
@login_required
def profile(request):
    return render(request, "users/profile.html", {'user': request.user})


def logout_view(request):
    auth_logout(request)
    return redirect('home')


@user_passes_test(lambda u: u.is_staff)
def admin_notifications(request):
    notes = AdminNotification.objects.all().order_by('-created_at')
    return render(request, "users/admin_notifications.html", {'notes': notes})
