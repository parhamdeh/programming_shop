from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from posts.selectors.category import get_all_categories
from posts.selectors.list_posts import get_all_posts
from django.core.paginator import Paginator

from posts.selectors.subscription import get_all_subscriptions

import logging

logger = logging.getLogger(__name__)


class HomeView(View):
    """
    Display the application's home page with
    paginated posts, categories, and subscriptions.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Retrieve posts, categories, and subscriptions,
        paginate the posts, and render the home page.
        """
        try:
            posts = get_all_posts()
            category = get_all_categories()
            subscription = get_all_subscriptions()
            paginator = Paginator(posts, 6)  
        except Exception as e:
            logger.exception(f"database error {e}")

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "home.html",
            {
                "page_obj": page_obj,
                "categories" : category,
                "subscriptions":subscription,
            },
        )

    