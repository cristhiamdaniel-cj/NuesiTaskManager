# backlog/api_urls.py
from django.urls import path
from . import api_auth

app_name = "api_backlog_auth"

urlpatterns = [
    # con slash (ya estaban)
    path("csrf/",   api_auth.csrf_view,  name="csrf"),
    path("login/",  api_auth.login_api,  name="login"),
    path("me/",     api_auth.me_api,     name="me"),
    path("logout/", api_auth.logout_api, name="logout"),

    # sin slash (parche 301)
    path("csrf",   api_auth.csrf_view),
    path("login",  api_auth.login_api),
    path("me",     api_auth.me_api),
    path("logout", api_auth.logout_api),
]
