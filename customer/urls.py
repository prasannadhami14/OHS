from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('index/',views.index),
    path("registerUser/",views.register_user,name="registerUser"),
    path("login/",views.login_user,name="logins"),
    path("loginform/",views.loginForm,name="login"),
    path("register/",views.registerForm,name="register"),
    path("logout/",views.logout_user,name="logout"),
    path("activate/<uidb64>/<token>",views.activate,name="activate"),


]
