from django.urls import path,include
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

url_threads = [
    path('newest/<str:filter>/', views.main_list, {'ordre': 'newest'}, name='newest_filter'),
    path('top', views.main_list, {'ordre': 'top', 'filter': 'tot'}, name='top'),
    path('top/<str:filter>/', views.main_list, {'ordre': 'top'}, name='top_filter'),
    path('commented', views.main_list, {'ordre': 'commented', 'filter': 'tot'}, name='commented'),
    path('commented/<str:filter>/', views.main_list, {'ordre': 'commented'}, name='commented_filter'),
    path('thread/<int:thread_id>/<str:order>/', views.veure_thread, name='veure_thread'),
    path('new', views.new_link, name='new_link'),
    path('new/thread', views.new_thread, name='new_thread'),
    path('create_link_thread', views.create_link_thread, name = 'create_link'),
    path('boost/<int:thread_id>/',views.boost_publicacio,name='boost_thread'),
    path('editar/thread/<int:thread_id>/', views.editar_thread, name='edit_thread'),
    path('editar/link/<int:thread_id>/', views.editar_link, name='editar_link'),
    path('eliminar/<int:thread_id>/', views.eliminar_publicacio, name='eliminar_publicacio'),

    path('votar/<int:thread_id>/', views.votar_publicacio, name='votar_thread'),
    path('boost/<int:thread_id>/',views.boost_thread,name='boost_thread'),
    path('cercador', views.view_cercador, {'ordre': 'newest', 'filter': 'tot'}, name='cercador'),
    path('cercador/newest/<str:filter>/', views.view_cercador, {'ordre': 'newest'},
         name='cercador_newest'),
    path('cercador/newest/', views.view_cercador, {'filter': 'tot', 'ordre': 'newest'},
         name='cercador_newest'),
    path('cercador/top/<str:filter>/', views.view_cercador, {'ordre': 'top'}, name='cercador_top'),
    path('cercador/top/', views.view_cercador, {'filter': 'tot', 'ordre': 'top'}, name='cercador_top'),
    path('cercador/commented/<str:filter>/', views.view_cercador, {'ordre': 'commented'},
         name='cercador_commented'),
    path('cercador/commented/', views.view_cercador, {'filter': 'tot', 'ordre': 'commented'},
         name='cercador_commented')
]

url_users = [
    path('u/<str:username>', views.view_user, name='view_user'),
    path('u/<str:username>/top', views.view_top, name='view_top'),
    path('u/<str:username>/newest', views.view_newest, name='view_newest'),
    path('u/<str:username>/commented', views.view_commented, name='view_commented'),
    path('settings/general', views.settings, name='settings'),
    path('settings/profile', views.edit_user, name='edit_user'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
]

url_comments = [
    path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('add_reply/<int:thread_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('like/<int:thread_id>/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike/<int:thread_id>/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('edit_comment/<int:thread_id>/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:thread_id>/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

url_magazines = [
    path('magazine/<int:magazine_id>/',views.veure_magazine, name='veure_magazine'),

    path('magazine/<int:magazine_id>/newest/<str:filter>/', views.veure_magazine, {'ordre': 'newest'}, name='veure_magazine_newest'),
    path('magazine/<int:magazine_id>/top/<str:filter>/', views.veure_magazine, {'ordre': 'top'}, name='veure_magazine_top'),
    path('magazine/<int:magazine_id>/comments/<str:filter>/', views.veure_magazine, {'ordre': 'comment'}, name='veure_magazine_comments'),




    path('magazines', views.all_magazines, name='all_magazines'),
    path('magazines/threads', views.all_magazines, {'ordre': 'threads'}, name='all_magazines_thread'),
    path('magazines/elements', views.all_magazines, {'ordre': 'elements'}, name='all_magazines_elements'),
    path('magazines/commented', views.all_magazines, {'ordre': 'commented'}, name='all_magazines_commented'),
    path('magazines/suscriptions', views.all_magazines, {'ordre': 'suscriptions'}, name='all_magazines_suscriptions'),

    path('newMagazine', views.new_magazine, name='new_magazine'),
]

urlpatterns = ([
    path('', views.main_list, {'ordre': 'newest', 'filter': 'tot'}, name='main'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + url_threads
               + url_users
               + url_comments
               + url_magazines)
