from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

# urlpatterns = [
#    path("endpoint1/", views.Endpoint1View.as_view(), name="endpoint1"),
# ]

urlpatterns = [
                  path('', views.main, name='main'),
                  path('new', views.new_link, name='new_link'),
                  path('create_link', views.create_link, name='create_link'),
                  path('top', views.top, name='top'),
                  path('commented', views.commented, name='commented'),
                  path('thread/<int:thread_id>/', views.veure_thread, name='veure_thread'),
                  path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
