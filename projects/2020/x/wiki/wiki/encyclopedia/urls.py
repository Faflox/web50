from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.entry_page, name="entry"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random_page, name="random"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("search", views.search, name="search"),
]
