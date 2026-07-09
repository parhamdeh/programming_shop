from django import forms
from posts.models import Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)