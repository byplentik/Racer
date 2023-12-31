from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from hcaptcha.fields import hCaptchaField

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'is_staff']


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(label='Номер телефрна', max_length=12, min_length=7)
    hcaptcha = hCaptchaField()


class VerificationCodeForm(forms.Form):
    code = forms.CharField(label='Введите проверочный код', max_length=6)


class PersonalСabinetForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'delivery_address', 'delivery_index']