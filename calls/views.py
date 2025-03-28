from rest_framework import viewsets, generics, status, filters
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from .models import Call
from .serializers import CallSerializer
from .filters import CallFilter  # Import the new filter

USE_JWT = getattr(settings, "USE_JWT", True)

if USE_JWT:
    DEFAULT_AUTH = [JWTAuthentication]
    DEFAULT_PERM = [IsAuthenticated]
else:
    DEFAULT_AUTH = [SessionAuthentication]
    DEFAULT_PERM = [AllowAny]


# Determine the default authentication and permission classes based on settings

# ✅ Pagination for CallListView
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size in query params
    max_page_size = 50  # Limit max page size

# ✅ List and create calls
class CallListCreateView(generics.ListCreateAPIView):
    queryset = Call.objects.all().order_by("-timestamp")
    serializer_class = CallSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    # Filtering and search support
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CallFilter
    search_fields = ["call_cid", "caller_number", "location"]
    ordering_fields = ["timestamp", "priority_level"]

    pagination_class = StandardResultsSetPagination


# ✅ Retrieve, update, or delete a call
class CallRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    lookup_field = "call_sid"  # or use "call_cid" if you prefer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

class CompleteCallView(APIView):
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERM

    def patch(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        call.complete_call()
        serializer = CallSerializer(call)
        return Response(serializer.data, status=status.HTTP_200_OK)