from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("following/", views.following, name="following"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/edit_description/", views.edit_description, name="edit_description"),
    path("create_post/", views.create_post, name="create_post"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("delete_post/", views.delete_post, name="delete_post"),
    path("follow_unfollow/", views.follow_unfollow, name="follow_unfollow"),
    path("like/", views.like, name="like"),
]
