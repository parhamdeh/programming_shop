from django import forms

from posts.models import Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "image",
            "video",
            "is_premium",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Post title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "Write your post..."
                }
            ),
        }