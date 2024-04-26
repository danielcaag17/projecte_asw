from django.urls import path
from .views import PublicacioTitleListView

urlpatterns = [
    path('publicacio/titles/', PublicacioTitleListView.as_view(), name='publicacio_titles'),
]