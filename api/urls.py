from django.urls import path
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
    path('like/<int:thread_id>/',views.like_thread,name='like_thread'),
    path('dislike/<int:thread_id>/',views.dislike_thread,name='dislike_thread'),
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
    path('u/usuari_predeterminat', views.view_user, name='view_user'),
    path('logout', views.logout_view, name='logout')
]

url_comments = [
    path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('add_reply/<int:thread_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('like/<int:thread_id>/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike/<int:thread_id>/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
]

url_magazines = [
    path('magazine/<int:magazine_id>/',views.veure_magazine, name='veure_magazine'),
    path('magazines', views.all_magazines, name='all_magazines'),
    path('newMagazine', views.new_magazine, name='new_magazine'),
]

urlpatterns = ([
    path('', views.main_list, {'ordre': 'newest', 'filter': 'tot'}, name='main'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + url_threads
               + url_users
               + url_comments
               + url_magazines)
