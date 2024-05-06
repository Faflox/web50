from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("create_post", views.create_post, name="create_post"),
    path("following/", views.following, name="following"),
    path("follow_unfollow/", views.follow_unfollow, name="follow_unfollow"),
]
