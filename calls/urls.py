from django.urls import path
from .views import CallListCreateView, CallRetrieveUpdateDestroyView, CompleteCallView

urlpatterns = [
    path("", CallListCreateView.as_view(), name="call-list-create"),
    path("<str:call_sid>/", CallRetrieveUpdateDestroyView.as_view(), name="call-detail"),
    path("<str:call_sid>/complete/", CompleteCallView.as_view(), name="call-complete"),
]