from django.urls import path
from . import views

url_users = [
    path('users/', views.UserView.as_view(), name='users'),

    path('u/<str:username>/', views.UserView.as_view(), name='view-user'),

    path('u/<str:username>/top/', views.UserView.as_view(), {'ordre': 'top'}, name='view-user'),
    path('u/<str:username>/newest/', views.UserView.as_view(), {'ordre': 'newest'}, name='view-user'),
    path('u/<str:username>/commented/', views.UserView.as_view(), {'ordre': 'commented'}, name='view-user'),

    path('u/<str:username>/top/<str:filtre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/newest/<str:filtre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/commented/<str:filtre>/', views.UserView.as_view(), name='view-user'),

    path('u/<str:username>/<str:element>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/<str:element>/<str:ordre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/<str:element>/<str:ordre>/<str:filtre>/', views.UserView.as_view(), name='view-user'),
]

urlpatterns = [

] + url_users
