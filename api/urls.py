from django.urls import path
from . import views

url_users = [
    path('u/<str:username>/', views.UserView.as_view(), name='view-user'),
    path('users/', views.UserView.as_view(), name='users'),

    path('u/<str:username>/threads/', views.UserThreadsView.as_view(), name='user-threads'),
]

urlpatterns = [

] + url_users
