from django.urls import path

from home.views.home_view import HomeView



app_name = "home"
urlpatterns = [
    path(route='', view=HomeView.as_view() ,name="home"),
]
