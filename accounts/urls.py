from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("delete/", views.delete, name="delete"),
    path("update/<int:pk>/", views.update, name="update"),
    path("idcheck/", views.id_check, name="id_check"),
    path('password_change/', views.password_change, name="password_change")
]

