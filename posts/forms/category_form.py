from django import forms
from mptt.forms import TreeNodeChoiceField

from posts.models import Category


class CategoryModelForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="----- Root Category -----",
    )

    class Meta:
        model = Category
        fields = ("name", "parent")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category name",
                }
            ),
            "parent": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # مرتب‌سازی درختی دسته‌بندی‌ها
        self.fields["parent"].queryset = Category.objects.all()