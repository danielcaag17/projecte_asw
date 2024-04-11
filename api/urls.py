from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

#urlpatterns = [
#    path("endpoint1/", views.Endpoint1View.as_view(), name="endpoint1"),
#]

urlpatterns = [
    path('', views.main, name='main'),
    path('new', views.new_link, name='new_link'),
path('new/thread', views.new_thread, name='new_thread'),
    path('create_link_thread', views.create_link_thread, name = 'create_link'),
    path('top',views.top, name='top'),
    path('commented',views.commented, name='commented'),
    path('thread/<int:thread_id>/',views.veure_thread,name='veure_thread')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
