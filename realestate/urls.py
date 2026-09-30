from django.urls import path
from realestate.views import (
    ApartmentListAPIView,
    ContractCancelAPIView,
    ContractCreateAPIView,
    ContractListAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path(
        'apartments/', ApartmentListAPIView.as_view(), name='apartment-list'
    ),
    path(
        'contracts/create/',
        ContractCreateAPIView.as_view(),
        name='contract-create',
    ),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('contracts/', ContractListAPIView.as_view(), name='contract-list'),
    path(
        'contracts/<int:pk>/cancel/',
        ContractCancelAPIView.as_view(),
        name='contract-cancel',
    ),
]