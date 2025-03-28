from django.urls import path
from .views import (
    SubjectListCreateView,
    SubjectSummaryView,
    SubjectRetrieveUpdateDestroyView,
    VehicleListCreateView,
    VehicleRetrieveUpdateDestroyView,
    DriversLicenseListCreateView,
    DriversLicenseDetailView,
    DriversLicenseByNumberView,
    DriversLicenseBySubjectView,
    AddressListCreateView, 
    AddressRetrieveUpdateDestroyView,
    DriversLicenseLookupView
)

urlpatterns = [
    path("subjects/", SubjectListCreateView.as_view(), name="subject-list-create"),
    path("subjects/<int:pk>/", SubjectRetrieveUpdateDestroyView.as_view(), name="subject-detail"),
    path("subjects/by_uid/<str:subject_uid>/", SubjectSummaryView.as_view(), name="subject-summary-by-uid"),
    path("vehicles/", VehicleListCreateView.as_view(), name="vehicle-list-create"),
    path("vehicles/<str:license_plate>/", VehicleRetrieveUpdateDestroyView.as_view(), name="vehicle-detail"),
    path("licenses/", DriversLicenseListCreateView.as_view(), name="license-list-create"),
    path("licenses/<int:pk>/", DriversLicenseDetailView.as_view(), name="license-detail"),
    path("licenses/number/<str:number>/", DriversLicenseByNumberView.as_view(), name="license-by-number"),
    path("licenses/subject/<int:subject_id>/", DriversLicenseBySubjectView.as_view(), name="license-by-subject"),
    path("licenses/lookup/", DriversLicenseLookupView.as_view(), name="license-lookup"),
    path("addresses/", AddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", AddressRetrieveUpdateDestroyView.as_view(), name="address-detail"),
]
