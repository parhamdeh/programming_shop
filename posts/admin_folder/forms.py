# django built_in
from django import forms
from django.core.exceptions import ValidationError

# third party
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from posts.models import Category, Post


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            "category",
            "author",
            "title",
            "content",
            "image",
            "video",
            "is_premium",
        )

    class Media:
        css = {
            "all": (
                "admin/css/post_form.css",
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["author"].queryset = (
            self.fields["author"]
            .queryset
            .filter(is_active=True)
            .only("id", "username")
            .order_by("username")
        )

        self.fields["category"].queryset = (
            Category.objects
            .only("id", "name")
            .order_by("name")
        )

        self.fields["title"].widget.attrs.update({
            "placeholder": "عنوان پست ...",
            "autocomplete": "off",
        })

        self.fields["content"].widget.attrs.update({
            "rows": 18,
        })

        self.fields["image"].help_text = (
            "JPG, PNG, WEBP - حداکثر 5MB"
        )

        self.fields["video"].help_text = (
            "MP4 - حداکثر 100MB"
        )

        self.helper = FormHelper()

        self.helper.form_tag = False

        self.helper.layout = Layout(

            Fieldset(
                "اطلاعات اصلی",

                Row(
                    Column("title"),
                    Column("category"),
                ),

                "author",

                "content",
            ),

            Fieldset(
                "رسانه",

                Row(
                    Column("image"),
                    Column("video"),
                ),
            ),

            Fieldset(
                "تنظیمات",

                "is_premium",
            ),
        )

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 5:
            raise ValidationError("عنوان حداقل باید ۵ کاراکتر باشد.")

        if len(title) > 50:
            raise ValidationError("عنوان بیش از حد طولانی است.")

        return title

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        if image.size > 5 * 1024 * 1024:
            raise ValidationError("حجم تصویر نباید بیشتر از ۵ مگابایت باشد.")

        return image

    def clean_video(self):
        video = self.cleaned_data.get("video")

        if not video:
            return video

        if video.size > 100 * 1024 * 1024:
            raise ValidationError("حجم ویدئو نباید بیشتر از ۱۰۰ مگابایت باشد.")

        return video

    def clean(self):
        cleaned_data = super().clean()

        image = cleaned_data.get("image")
        video = cleaned_data.get("video")
        category = cleaned_data.get("category")
        premium = cleaned_data.get("is_premium")

        if not image and not video:
            raise ValidationError(
                "حداقل یک تصویر یا ویدئو باید انتخاب شود."
            )

        if premium and category is None:
            self.add_error(
                "category",
                "برای پست ویژه انتخاب دسته‌بندی الزامی است."
            )

        return cleaned_data