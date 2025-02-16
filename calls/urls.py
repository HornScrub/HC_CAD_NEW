from django.urls import path
from .views import CallCreateView, CallUpdateView, CallInteractionCreateView

urlpatterns = [
    path('calls/', CallCreateView.as_view(), name='call-create'),
    path('calls/<str:call_sid>/', CallUpdateView.as_view(), name='call-update'),
    path('calls/<str:call_sid>/interactions/', CallInteractionCreateView.as_view(), name='call-interaction'),
]
