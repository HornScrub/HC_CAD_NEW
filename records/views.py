from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Vehicle, Subject, DriversLicense, Address
from .serializers import VehicleSerializer, SubjectSummarySerializer, SubjectDetailSerializer, DriversLicenseSerializer, AddressSerializer
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

USE_JWT = getattr(settings, "USE_JWT", True)
if USE_JWT:
    from rest_framework_simplejwt.authentication import JWTAuthentication
    DEFAULT_AUTH = [JWTAuthentication]
    DEFAULT_PERM = [IsAuthenticated]
else:
    DEFAULT_AUTH = [SessionAuthentication]
    DEFAULT_PERM = [AllowAny]

# ✅ List + Create Vehicles
class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all().order_by("license_plate")
    serializer_class = VehicleSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["license_plate", "make", "model", "color"]
    ordering_fields = ["license_plate", "year"]

# ✅ Retrieve + Update + Delete Vehicle
class VehicleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = "license_plate"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# List all subjects OR create new one
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailSerializer  # Used for both list/create
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# Retrieve, update, or delete a subject
class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# View by UID (optional)
class SubjectSummaryView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSummarySerializer
    lookup_field = "subject_uid"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# List + Create
class DriversLicenseListCreateView(generics.ListCreateAPIView):
    queryset = DriversLicense.objects.all()
    serializer_class = DriversLicenseSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# Retrieve + Update + Delete by primary key
class DriversLicenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DriversLicense.objects.all()
    serializer_class = DriversLicenseSerializer
    lookup_field = "pk"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

class DriversLicenseByNumberView(generics.RetrieveAPIView):
    queryset = DriversLicense.objects.all()
    serializer_class = DriversLicenseSerializer
    lookup_field = 'license_number'  # or 'number', depending on your model

class DriversLicenseBySubjectView(generics.ListAPIView):
    serializer_class = DriversLicenseSerializer

    def get_queryset(self):
        subject_id = self.kwargs["subject_id"]
        return DriversLicense.objects.filter(subject__id=subject_id)

class DriversLicenseLookupView(generics.ListAPIView):
    serializer_class = DriversLicenseSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name", "").strip()
        last_name = self.request.query_params.get("last_name", "").strip()
        dob = self.request.query_params.get("dob", "").strip()

        qs = DriversLicense.objects.all()
        print("FILTERING:", first_name, last_name, dob)

        if first_name:
            qs = qs.filter(first_name__iexact=first_name)

        if last_name:
            qs = qs.filter(last_name__iexact=last_name)

        if dob:
            qs = qs.filter(subject__date_of_birth=dob)

        print("FOUND:", qs.count())
        return qs

# List + Create Addresses
class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all().order_by("city", "street")
    serializer_class = AddressSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

# Retrieve + Update + Delete a single Address
class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "pk"
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM



