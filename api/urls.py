from django.urls import path
from . import views

urlpatterns = [
    path('<str:filter>/<str:ordre>/', views.LlistaThreadLinks.as_view(), name='llistar_publicacions'),
]
