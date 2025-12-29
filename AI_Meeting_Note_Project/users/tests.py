from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import CustomUser, OTP

class UsersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            is_active=True
        )

    # -------------------- Signup / Login Pages --------------------
    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    # -------------------- OTP Creation & Verification --------------------
    def test_create_otp_for_user(self):
        otp = OTP.create_otp(self.user, valid_seconds=60)
        self.assertTrue(otp.is_valid())
        self.assertEqual(otp.user, self.user)

    def test_verify_login_otp_success(self):
        otp = OTP.create_otp(self.user, valid_seconds=60)
        session = self.client.session
        session['pending_login_user_id'] = self.user.id
        session['pending_login_otp_uuid'] = str(otp.uuid)
        session.save()
        response = self.client.post(reverse('verify_login_otp'), {'otp': otp.code})
        self.assertRedirects(response, reverse('dashboard'))

    def test_verify_login_otp_expired(self):
        otp = OTP.create_otp(self.user, valid_seconds=-1)  # already expired
        session = self.client.session
        session['pending_login_user_id'] = self.user.id
        session['pending_login_otp_uuid'] = str(otp.uuid)
        session.save()
        response = self.client.post(reverse('verify_login_otp'), {'otp': otp.code})
        self.assertRedirects(response, reverse('resend_login_otp'))

    # -------------------- Password Reset --------------------
    def test_password_reset_request(self):
        response = self.client.post(reverse('password_reset_request'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertIn('password_reset_user_id', self.client.session)

    def test_password_reset_confirm(self):
        otp = OTP.create_otp(self.user)
        session = self.client.session
        session['password_reset_user_id'] = self.user.id
        session['password_reset_otp_uuid'] = str(otp.uuid)
        session.save()
        response = self.client.post(reverse('password_reset_confirm'), {
            'otp': otp.code,
            'new_password': 'newpass123',
            'new_password2': 'newpass123'
        })
        self.assertRedirects(response, reverse('login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    # -------------------- Email Change --------------------
    def test_email_change_request_and_verify(self):
        self.client.login(email=self.user.email, password='testpass123')
        response = self.client.post(reverse('email_change_request'), {'new_email': 'newemail@example.com'})
        self.assertRedirects(response, reverse('email_change_verify'))

        otp = OTP.objects.filter(user=self.user, is_used=False).first()
        session = self.client.session
        session['email_change_new_email'] = 'newemail@example.com'
        session['email_change_otp_uuid'] = str(otp.uuid)
        session.save()
        response = self.client.post(reverse('email_change_verify'), {'otp': otp.code})
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
