# incidents/urls.py
from django.urls import path
from .views import IncidentListCreateView, IncidentRetrieveUpdateDestroyView, TrafficStopListCreateView, TrafficStopRetrieveUpdateDestroyView

urlpatterns = [
    path("trafficstops/", TrafficStopListCreateView.as_view(), name="trafficstop-list-create"),
    path("trafficstops/<str:incident_id>/", TrafficStopRetrieveUpdateDestroyView.as_view(), name="trafficstop-detail"),
    path("", IncidentListCreateView.as_view(), name="incident-list-create"),
    path("<str:incident_id>/", IncidentRetrieveUpdateDestroyView.as_view(), name="incident-detail"),
]
