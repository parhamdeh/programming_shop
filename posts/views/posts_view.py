from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.selectors.post_detail import get_post_detail, get_related_posts, check_favorit, check_post_is_premium
from posts.services.post import create_comment, create_favorit_post, delete_comment_post, delete_favorit_post
from posts.forms.post_detail_form import CommentForm
from posts.selectors.subscription import get_user_subscription_with_user

import logging

logger = logging.getLogger(__name__)



class PostDetailView(LoginRequiredMixin, View):
    """
    Display the post detail page and handle comment submission.
    """

    template_name = 'detail.html'
    form_class = CommentForm
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        post_id = kwargs.get("post_id")

        if not check_post_is_premium(post_id=post_id, user_id=request.user.id):
            messages.warning(request, "this post is premium please buy a subsciption first!")
            return redirect("home:home")


        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        """
        Retrieve a post with its related posts and render
        the post detail page.
        """
        try:
            post = get_post_detail(post_id)
            is_favorit = check_favorit(post=post, user=request.user)
            
            related_posts = get_related_posts(post)
        except Exception as e:
            logger.exception(
            f"database error: {e}"
        )

        form = CommentForm()

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "post": post,
                "related_posts": related_posts,
                "form": form,
                "is_favorite":is_favorit,
            },
        )
    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        """
        Validate the submitted comment form and create
        a new comment for the selected post.
        """
        if not request.user.is_authenticated:

            messages.error(
                request,
                "Please login first."
            )

            return redirect("users:login")

        form = CommentForm(request.POST)

        if form.is_valid():
            try:
                comment = create_comment(
                    user=request.user,
                    post_id=post_id,
                    content=form.cleaned_data["content"],
                )
            except Exception as e:
                logger.exception(
                f"database error: {e}"
            )

            logger.info(f"{request.user} added a comment {comment.content}")
            messages.success(
                request,
                "Comment added successfully."
            )

        return redirect(
            "posts:detail",
            post_id=post_id,
        )

    
class PostFavoritView(LoginRequiredMixin, View):
    """
    Add the selected post to the authenticated user's
    favorites list.
    """
    def get(self, request: HttpRequest, post_id:int) -> HttpResponse:
        """
        Create a favorite record for the specified post.
        """
        try:
            create_favorit_post(user=request.user, post_id=post_id)
        except Exception as e:
            logger.exception(
                f"database error: {e}"
            )

        logger.info(f"{request.user} liked post: {post_id}")
        messages.success(
                request,
                "Post added To Favorits successfully."
            )
        return redirect("posts:detail", post_id)

class DeleteCommetntView(LoginRequiredMixin, View):
    """
        Delete the authenticated user's comment
        from the selected post.
        
    """
    def get(self, request: HttpRequest, post_id:int) -> HttpResponse:
        """
        Remove the user's comment from the specified post.
        """
        try:
            delete_comment_post(user=request.user, post_id=post_id)
        except Exception as e:
            logger.exception(
                f"database error: {e}"
            )

        logger.info(f"{request.user} deleted comment in post: {post_id}")    
        messages.success(
                request,
                "comment deleted successfully."
            )
        return redirect("posts:detail", post_id)


class DeleteFavorit(LoginRequiredMixin, View):
    """
    Remove the selected post from the authenticated user's
    favorites list.
    """
    
    def get(self, request: HttpRequest, post_id:int) -> HttpResponse:
        """
        Delete the favorite relationship for the specified post.
        """
        try:
            delete_favorit_post(user=request.user, post_id=post_id)
        except Exception as e:
            logger.exception(
                f"database error: {e}"
            )
        
        logger.info(f"{request.user} unliked {post_id}")
        messages.success(
                request,
                "Post deleted From Favorits successfully."
            )
        return redirect("posts:detail", post_id)




