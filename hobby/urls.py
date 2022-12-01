from django.urls import path
from . import views

app_name = "hobby"

urlpatterns = [
    path("create", views.create, name="create"),
    path('test', views.test, name='test'),
    path("index/<str:category_name>/", views.index, name="index"),
    path("index/<str:tag_name>/", views.tag, name="tag"),
]
