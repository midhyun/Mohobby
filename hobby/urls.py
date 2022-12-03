from django.urls import path
from . import views

app_name = "hobby"

urlpatterns = [
    path("create", views.create, name="create"),
    path('test', views.test, name='test'),
    path('<int:hobby_pk>', views.detail, name='detail'),
    path('<int:hobby_pk>/call', views.call, name='call'),
    path('<int:hobby_pk>/<int:user_pk>/approve', views.approve, name='approve'),
    path('<int:hobby_pk>/<int:user_pk>/reject', views.reject, name='reject'),
    path('<int:hobby_pk>/comment_create', views.comment_create, name='comment_create'),
    path("index/<str:category_name>/", views.index, name="index"),
    path("index/tag/<str:tag_name>/", views.tag, name="tag"),
]
