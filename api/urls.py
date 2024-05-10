from django.urls import path
from . import views

urlmagazines = [
    path('magazines/<str:ordre>/', views.LlistarMagazines.as_view(), name='llistar_magazines'),
    path('magazines/', views.CrearMagazine.as_view(), name='crear_magazine')
]

url_comentaris = [
    path('publicacions/<int:id_thread>/comments/<str:ordre>/', views.VeureComentarisPublicacio.as_view(),
         name='veure-comentaris-publicacio'),
    path('publicacions/<int:id_thread>/create_comment/', views.CrearComentari.as_view(), name='crear-comentari'),
    path('comments/create_reply/<int:id_comment>/', views.CrearComentariResposta.as_view(),
         name='crear-comentari-resposta'),
    path('comments/vote/<int:id_comment>/<str:tipus_vot>/', views.VotarComentari.as_view(), name='votar-comentari'),
    path('comments/<int:id_comment>/', views.ComentariIndividual.as_view(), name='obtenir-comentari'),
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

url_threads = [
    path('llistar/<str:filter>/<str:ordre>/', views.LlistaThreadLinks.as_view(), name='llistar_publicacions'),
    path('thread/',views.CrearThread.as_view(), name='crear_thread'),
    path('link/',views.CrearLink.as_view(),name='crear_link'),
    path('publicacions/votar/<int:id_publicacio>/<str:tipus_vot>/',views.VotarPublicacio.as_view(),name='votar_publicacio'),
    path('cercador/<str:filter>/<str:ordre>/',views.CercarPublicacions.as_view(),name='cercador'),
    path('publicacions/<int:id_publicacio>/',views.PublicacioIndividual.as_view(),name='obtenir_publicacio'),
    path('publicacions/boost/<int:id_publicacio>/',views.ImpulsarPublicacio.as_view(),name='obtenir_publicacio')
]

urlpatterns = [

] + urlmagazines + url_users + url_comentaris + url_threads
