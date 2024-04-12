from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.main_list,{'ordre':'newest','filter':'tot'}, name='main'),
    path('newest/<str:filter>/', views.main_list,{'ordre':'newest'}, name='newest_filter'),
    path('top',views.main_list,{'ordre':'top','filter':'tot'}, name='top'),
    path('top/<str:filter>/', views.main_list,{'ordre':'top'}, name='top_filter'),
    path('commented',views.main_list,{'ordre':'commented','filter':'tot'}, name='commented'),
    path('commented/<str:filter>/', views.main_list,{'ordre':'commented'}, name='commented_filter'),
    path('thread/<int:thread_id>/',views.veure_thread,name='veure_thread'),
    path('new', views.new_link, name='new_link'),
    path('u/usuari_predeterminat', views.view_user, name='view_user'),
    path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('add_reply/<int:thread_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('new/thread', views.new_thread, name='new_thread'),
    path('create_link_thread', views.create_link_thread, name = 'create_link'),
    path('like/<int:thread_id>/',views.like_thread,name='like_thread'),
    path('dislike/<int:thread_id>/',views.dislike_thread,name='dislike_thread'),
    path('boost/<int:thread_id>/',views.boost_thread,name='boost_thread')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
