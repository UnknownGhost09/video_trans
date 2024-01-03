from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home),
    path('download/<str:pk>/',views.download),
    path('login',views.login),
    path('logout',views.logout)
   
]
