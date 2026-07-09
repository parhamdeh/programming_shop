from django import forms


class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):

        cleaned_data = super().clean()

        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data