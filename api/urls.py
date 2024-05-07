from django.urls import path
from . import views

urlmagazines = [
    path('magazines/<str:ordre>/', views.LlistarMagazines.as_view(), name='llistar_magazines')
]

url_comentaris = [
    path('publicacions/<int:id_thread>/comments/', views.VeureComentarisPublicacio.as_view(),
         name='veure-comentaris-publicacio'),
    path('publicacions/<int:id_thread>/create_comment/', views.CrearComentariPublicacio.as_view(),
         name='crear-comentari-publicacio'),
    path('publicacions/<int:id_thread>/comments/<int:id_comment>/create_reply/', views.CrearComentariResposta.as_view(),
         name='crear-comentari-resposta'),
]

url_users = [
    path('users/', views.UserView.as_view(), name='users'),

    path('u/<str:username>/', views.UserView.as_view(), name='view-user'),

    path('u/<str:username>/top/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/newest/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/commented/', views.UserView.as_view(), name='view-user'),

    path('u/<str:username>/top/<str:filtre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/newest/<str:filtre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/commented/<str:filtre>/', views.UserView.as_view(), name='view-user'),

    path('u/<str:username>/<str:element>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/<str:element>/<str:ordre>/', views.UserView.as_view(), name='view-user'),
    path('u/<str:username>/<str:element>/<str:ordre>/<str:filtre>/', views.UserView.as_view(), name='view-user'),

    path('settings/profile/<str:username>/', views.UserView.as_view(), name='edit_user'),
]

urlpatterns = [
    #path('<str:filter>/<str:ordre>/', views.LlistaThreadLinks.as_view(), name='llistar_publicacions'),
    path('threads/',views.CrearThread.as_view(), name='crear_thread'),
    path('links/',views.CrearLink.as_view(),name='crear_link'),
] + urlmagazines + url_users + url_comentaris
