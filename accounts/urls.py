from django.urls import path
from . import views

urlpatterns = [
    path("login/" , views.loginuser , name='login'), 
    path("register/" , views.register , name='register'),
    path("logout/" , views.logoutuser , name='logout'),
    path("verify_code/" , views.verify_code , name='verify_code'),
    path("verify_2fa_code/" , views.verify_2fa_code , name='verify_2fa_code'),
]