# units/urls.py
from django.urls import path
from .views import UnitListCreateView, UnitDetailView

urlpatterns = [
    path('', UnitListCreateView.as_view(), name='unit-list-create'),
    path('<str:identifier>/', UnitDetailView.as_view(), name='unit-detail'),
]
