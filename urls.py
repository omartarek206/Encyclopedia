from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),

    path("<str:my_Entry>", views.visit_Entry, name="visit_Entry")
]
