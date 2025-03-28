# incidents/views.py

from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from .models import Incident, TrafficStop
from .serializers import IncidentSerializer, TrafficStopSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ✅ Auth handling
USE_JWT = getattr(settings, "USE_JWT", True)
if USE_JWT:
    DEFAULT_AUTH = [JWTAuthentication]
    DEFAULT_PERM = [IsAuthenticated]
else:
    DEFAULT_AUTH = [SessionAuthentication]
    DEFAULT_PERM = [AllowAny]


# ✅ List and create incidents
class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all().order_by("-created_at")
    serializer_class = IncidentSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["incident_id", "title", "location", "status"]
    ordering_fields = ["created_at", "priority_level"]


# ✅ Retrieve, update, and delete an incident
class IncidentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    lookup_field = "incident_id"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

class TrafficStopListCreateView(generics.ListCreateAPIView):
    queryset = TrafficStop.objects.all().order_by("-timestamp")
    serializer_class = TrafficStopSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["incident_id", "location", "reason"]
    ordering_fields = ["timestamp"]


class TrafficStopRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrafficStop.objects.all()
    serializer_class = TrafficStopSerializer
    lookup_field = "incident_id"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM