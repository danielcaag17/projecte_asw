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
    path('create_link', views.create_link, name = 'create_link'),
    path('top',views.top, name='top'),
    path('commented',views.commented, name='commented'),
    path('magazines',views.view_magazines, name='view_magazines')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
