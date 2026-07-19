from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from users.models import BaseUserModel


class BaseUserAdminForm(forms.ModelForm):

    class Meta:
        model = BaseUserModel
        fields = (
            "username",
            "phone",
            "password",
            "is_staff",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                "اطلاعات کاربر",
                "username",
                "phone",
                "password",
            ),
            Fieldset(
                "سطح دسترسی",
                "is_staff",
                "is_active",
            ),
        )

        self.fields["username"].help_text = "نام کاربری باید یکتا باشد."

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) < 4:
            raise forms.ValidationError("نام کاربری حداقل ۴ کاراکتر باشد.")

        return username

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone")
        username = cleaned_data.get("username")

        if username and phone:
            if username == str(phone):
                raise forms.ValidationError(
                    "نام کاربری و شماره تلفن نباید یکسان باشند."
                )

        return cleaned_data