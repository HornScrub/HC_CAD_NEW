# units/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Unit
from .serializers import UnitSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

USE_JWT = getattr(settings, "USE_JWT", True)

if USE_JWT:
    DEFAULT_AUTH = [JWTAuthentication]
    DEFAULT_PERM = [IsAuthenticated]
else:
    DEFAULT_AUTH = [SessionAuthentication]
    DEFAULT_PERM = [AllowAny]


class UnitDetailView(APIView):
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    @swagger_auto_schema(
        operation_description="Retrieve a unit by identifier",
        responses={200: UnitSerializer()}
    )

    def get(self, request, identifier):
        unit = get_object_or_404(Unit, identifier=identifier)
        serializer = UnitSerializer(unit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=UnitSerializer,
        operation_description="Fully update a unit",
        responses={200: UnitSerializer()}
    )

    def put(self, request, identifier):
        unit = get_object_or_404(Unit, identifier=identifier)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UnitSerializer,
        operation_description="Partially update a unit",
        responses={200: UnitSerializer()}
    )

    def patch(self, request, identifier):
        unit = get_object_or_404(Unit, identifier=identifier)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UnitListCreateView(APIView):
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    @swagger_auto_schema(
        operation_description="List all units",
        responses={200: UnitSerializer(many=True)}
    )

    def get(self, request):
        """List all units"""
        units = Unit.objects.all().order_by("name")
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=UnitSerializer,
        operation_description="Create a new unit",
        responses={201: UnitSerializer()}
    )

    def post(self, request):
        """Create a new unit"""
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
