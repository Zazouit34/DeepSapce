from django.urls import path
from . import views

urlpatterns = [
    path("",views.register,name="register"),
    path("login",views.login_view,name="login"),
    path("profile",views.profile,name="profile"),
    path("logout",views.logout_view,name="logout"),
    path("delete-account",views.deleteAccount,name="delete_account"),
    
]