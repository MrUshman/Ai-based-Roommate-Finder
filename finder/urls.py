from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("profiles/", views.profile_list, name="profiles"),
    path("profiles/create/", views.profile_create, name="profile_create"),
    path("profiles/<int:pk>/", views.profile_detail, name="profile_detail"),
    path("rooms/", views.room_list, name="rooms"),
    path("rooms/create/", views.room_create, name="room_create"),
    path("rooms/<int:pk>/", views.room_detail, name="room_detail"),
    path("matches/", views.matches, name="matches"),
    path("calculator/", views.calculator, name="calculator"),
    path("interests/", views.interest_list, name="interests"),
    path("interests/send/", views.send_interest, name="send_interest"),
    path("login/", auth_views.LoginView.as_view(template_name="finder/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"),
]
