from django.urls import path
from .views import CallListView, CallCreateView, CallUpdateView, CallInteractionCreateView

urlpatterns = [
    path("calls/", CallListView.as_view(), name="get_calls"),  # No "/api/" prefix here!
    path("calls/create/", CallCreateView.as_view(), name="call-create"),
    path("calls/<str:call_sid>/", CallUpdateView.as_view(), name="call-update"),
    path("calls/<str:call_sid>/interactions/", CallInteractionCreateView.as_view(), name="call-interaction"),
]
