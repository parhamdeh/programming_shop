from django import forms

from posts.models import Comments


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comments

        fields = [
            "content",
        ]