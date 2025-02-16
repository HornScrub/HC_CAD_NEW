from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Call, CallInteraction
from .serializers import CallSerializer, CallInteractionSerializer

# Create your views here.

# createCall | /api/calls/
# - Creates new call record when dispatch starts
# - - INPUT: POST
# - - OUTPUT: new call record created

class CallCreateView(generics.CreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# Retrieve or update a call record
class CallUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # get | /api/calls/<call_sid>/
    # - Retrieve call status and details
    # - - INPUT: PUT w/ call_sid and members to change
    # - - OUTPUT: Updates call at call_sid
    def get(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        serializer = CallSerializer(call)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # put | /api/calls/<call_sid>/interactions
    # - Update call status and/or details
    # - - INPUT: 
    # - - OUTPUT: Updates call_sid log
    def put(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        serializer = CallSerializer(call, data=request.data, partial=True) # Allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Log a conversation interaction
class CallInteractionCreateView(generics.CreateAPIView):
    serializer_class = CallInteractionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, call_sid):
        call = get_object_or_404(Call, call_sid=call_sid)
        data = request.data.copy()
        data['call'] = call.id
        serializer = CallInteractionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)