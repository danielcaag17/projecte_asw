from django.urls import path
from . import views

urlpatterns = [
    path("endpoint1/", views.Endpoint1View.as_view(), name="endpoint1"),
]