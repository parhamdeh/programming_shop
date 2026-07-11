from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from posts.models import Post
from posts.selectors.category import get_category_by_id

import logging

logger = logging.getLogger(__name__)


class CategoryDetailView(LoginRequiredMixin, View):
    """
    Display the details of a category along with
    its related posts.
    """

    template_name = "category/detail.html"
    def get(self, request: HttpRequest, category_id: int) -> HttpResponse:
        """
        Retrieve the requested category and render
        the category detail page.
        """
        try:
            category = get_category_by_id(category_id=category_id).first()
        except Exception as e:
            logger.exception(
                f"database error: {e}"
        )
        if not category:
            raise ObjectDoesNotExist("category not found")
        
        if category.parent is None:
            posts = Post.objects.filter(
                Q(category=category) |
                Q(category__parent=category)
            ).distinct()
        else:
            posts = category.posts.all()
        

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          'category' : category,
                          'posts' : posts,

                      })