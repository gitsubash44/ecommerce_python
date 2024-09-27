from django.urls import path
from accounts import views

urlpatterns = [
    path('user_login', views.user.login,name="user_login" ),
    path('user_register', views.user.register,name="user_register" ),
    path('user_logout', views.user.logout,name="user_logout" ),
]
