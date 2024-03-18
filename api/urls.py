from django.urls import path
from . import views
<<<<<<< HEAD

urlpatterns = [
    path("endpoint1/", views.Endpoint1View.as_view(), name="endpoint1"),
]
=======
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/', views.main, name='main'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 568fff0b83ca6b67f3ef720df537872f2161d26c
