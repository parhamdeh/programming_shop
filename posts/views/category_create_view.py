import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from posts.forms.category_form import CategoryModelForm
from posts.models import Category
from posts.services.category import create_category


class CreateCategory(View):
    """
    Display the category creation form and handle
    the creation of new categories.
    """
    form_class = CategoryModelForm
    template_name = "category/create_category.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """
        Ensure that only authenticated staff users
        can access this view.
        """
        if not request.user.is_authenticated:
            return redirect("users:login")

        if not request.user.is_staff:   
            messages.error(request, "You don't have permission to access this page.")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render an empty category creation form.
        """
        form = self.form_class()

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          'form':form
                      })

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Validate the submitted form and create
        a new category.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                category = create_category(data=form.cleaned_data)
            except Exception as e:
                logger.exception(
                    f"database error: {e}"
            )
            logger.info(
                f"New category category: {category.name}"
            )
            messages.success(
                    request,
                    "Category added successfully."
                )
            return redirect("home:home")
        messages.error(
            request,
            "there is a error"
        )
        return render(request=request,
                      template_name=self.template_name,
                      context={
                          'form':form,
                      })


