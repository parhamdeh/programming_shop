# third party packages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
# django built in
from django import forms

# local apps
from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False  

        self.helper.layout = Layout(
            Row(
                Column("title", css_class="col-6"),
                Column("category", css_class="col-6"),
            ),
            "content",
            Row(
                Column("image", css_class="col-6"),
                Column("video", css_class="col-6"),
            ),
            "is_premium",
        )