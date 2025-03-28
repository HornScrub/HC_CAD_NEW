from django.urls import path
from .views import InteractionLogView

urlpatterns = [
    path("log/<str:call_sid>/", InteractionLogView.as_view(), name="log-interaction"),
]