from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<int:community_pk>/detail", views.detail, name="detail"),
    path("<int:community_pk>/update", views.update, name="update"),
]
