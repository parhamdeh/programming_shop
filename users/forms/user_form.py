from django import forms

from users.models import BaseUserModel
from utils.validators import LetterValidator, NumberValidator, SpecialCharValidator
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
        validators=[
            LetterValidator(),
            NumberValidator(),
            SpecialCharValidator(),
        ]
    )

    class Meta:
        model = BaseUserModel
        fields = [
            "username",
            "phone",
            "password",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        phone = cleaned_data.get("phone")
        if phone and len(str(phone).replace("+98", "0")) > 11:
            raise forms.ValidationError("phone number is not valid")
        cleaned_data["phone"] = str(phone).replace("+98", "0")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords must match."
                )

        return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)

    #     user.set_password(
    #         self.cleaned_data["password"]
    #     )

    #     if commit:
    #         user.save()

    #     return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password,
            )

            if user is None:
                raise forms.ValidationError(
                    "Username or password is incorrect."
                )

            self.user = user

        return cleaned_data

class VerifyOtpForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter verification code"
            }
        )
    )