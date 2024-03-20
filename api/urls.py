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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
