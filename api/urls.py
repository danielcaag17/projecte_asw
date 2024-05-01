from django.urls import path
from . import views

urlpatterns = [
    path('<str:filter>/<str:ordre>/', views.Llista_threads_links.as_view(), name='llistar_publicacions'),
]
