from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Call
from interactions.models import Interaction
from units.models import Unit
from calls.serializers import CallSerializer  # your existing serializer
from .serializers import InteractionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

USE_JWT = getattr(settings, "USE_JWT", True)
if USE_JWT:
    DEFAULT_AUTH = [JWTAuthentication]
    DEFAULT_PERM = [IsAuthenticated]
else:
    DEFAULT_AUTH = [SessionAuthentication]
    DEFAULT_PERM = [AllowAny]


class InteractionLogView(APIView):
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    @swagger_auto_schema(
        request_body=InteractionSerializer,
        responses={201: InteractionSerializer}
    )

    def post(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        data = request.data.copy()
        data["call"] = call.id

        if call.incident:
            data["incident"] = call.incident.id  # auto-attach incident if one exists

        serializer = InteractionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
