# users/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class SignupForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(required=False)
    nid_number = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    picture = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=(('Male','Male'),('Female','Female'),('Other','Other')), required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already used.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=10, label='OTP')


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class PasswordResetConfirmForm(forms.Form):
    otp = forms.CharField(max_length=10)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')


class EmailChangeRequestForm(forms.Form):
    new_email = forms.EmailField()
