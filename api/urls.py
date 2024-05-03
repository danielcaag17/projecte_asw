from django.urls import path
from . import views

urlpatterns = [
    path('<str:filter>/<str:ordre>/', views.LlistaThreadLinks.as_view(), name='llistar_publicacions'),
    path('threads/',views.crear_thread.as_view(), name='crear_thread'),
]
