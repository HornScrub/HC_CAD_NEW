from rest_framework import viewsets, generics, status, filters
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import Call, CallInteraction
from .serializers import CallSerializer, CallInteractionSerializer
from .filters import CallFilter  # Import the new filter

# ✅ Pagination for CallListView
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size in query params
    max_page_size = 50  # Limit max page size

# ✅ View for listing calls with filtering, search, ordering, and pagination
class CallListView(generics.ListAPIView):
    queryset = Call.objects.all().order_by("-timestamp")
    serializer_class = CallSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Apply custom filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CallFilter  # Use the custom filter class instead of filterset_fields
    search_fields = ["incident_number", "location"]
    ordering_fields = ["timestamp", "priority_level"]

    # ✅ Enable pagination
    pagination_class = StandardResultsSetPagination

# ✅ Create a new call
class CallCreateView(generics.CreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# ✅ Retrieve, update, or partially update a call
class CallUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # ✅ Retrieve a call
    def get(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        serializer = CallSerializer(call)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ✅ Full update (PUT)
    def put(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        serializer = CallSerializer(call, data=request.data)  # Require all fields for PUT
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Partial update (PATCH)
    def patch(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        serializer = CallSerializer(call, data=request.data, partial=True)  # Allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Log a conversation interaction
class CallInteractionCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, call_sid):
        """Create a new call interaction"""
        call = get_object_or_404(Call, call_sid=call_sid)
        data = request.data.copy()
        data["call"] = call.id
        serializer = CallInteractionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, interaction_id):
        """Update an existing interaction (e.g., add message later)"""
        interaction = get_object_or_404(CallInteraction, id=interaction_id)
        serializer = CallInteractionSerializer(interaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallInteractionListView(generics.ListAPIView):
    queryset = CallInteraction.objects.all().order_by("-timestamp")
    serializer_class = CallInteractionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["call", "speaker"]
    search_fields = ["message"]
    ordering_fields = ["timestamp"]
    pagination_class = StandardResultsSetPagination
