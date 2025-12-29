import random
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from django.conf import settings
from .models import EmailOTP


def generate_otp():
    """Generate a 6-digit numeric OTP"""
    return str(random.randint(100000, 999999))


def send_otp_email(user, purpose):
    """
    Send OTP to user via email and save in database.
    OTP validity is read from .env via settings.OTP_VALID_SECONDS
    """

    otp_code = generate_otp()

    # Read OTP valid seconds from settings
    valid_seconds = getattr(settings, "OTP_VALID_SECONDS", 60)

    expires_at = timezone.now() + timedelta(seconds=valid_seconds)

    # Delete old OTPs for this user and purpose
    EmailOTP.objects.filter(user=user, purpose=purpose).delete()

    # Create new OTP entry
    EmailOTP.objects.create(
        user=user,
        otp=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )

    # Send email
    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP is {otp_code}. It is valid for {valid_seconds} seconds.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
