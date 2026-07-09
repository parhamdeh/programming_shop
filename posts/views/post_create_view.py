from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from posts.services.post import create_post
from posts.forms.post_create_form import CreatePostForm

import logging

logger = logging.getLogger(__name__)


class CreatePost(View):
    """
    Display the post creation form and handle the creation
    of new posts.
    """
    form_class = CreatePostForm
    template_name = "create_post.html"

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
        Render an empty post creation form.
        """
        
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Validate the submitted form and create
        a new post.
        """
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            try:
                post = create_post(author=request.user, category=form.cleaned_data["category"], title=form.cleaned_data["title"], content=form.cleaned_data["content"], image=form.cleaned_data["image"], video=form.cleaned_data["video"], is_premium=form.cleaned_data["is_premium"])
            except Exception as e:
                logger.exception(
                f"database error: {e}"
            )
            logger.info(f"post created : {post.title}")
            messages.success(request, "Post created successfully.")
            return redirect("posts:detail", post.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )