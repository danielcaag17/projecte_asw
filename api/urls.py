from django.urls import path
from . import views

urlmagazines = [
    path('magazines/<str:ordre>/', views.LlistarMagazines.as_view(), name='llistar_magazines')
]

urlpatterns = [
    #path('<str:filter>/<str:ordre>/', views.LlistaThreadLinks.as_view(), name='llistar_publicacions'),
    path('threads/',views.CrearThread.as_view(), name='crear_thread'),
    path('links/',views.CrearLink.as_view(),name='crear_link'),
] + urlmagazines


