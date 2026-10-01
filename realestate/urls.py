from django.urls import path

from realestate.views import (
    ApartmentListAPIView,
    ApartmentDetailAPIView,
    ContractCancelAPIView,
    ContractCreateAPIView,
    ContractListAPIView,
    RegisterAPIView,
)

from realestate.admin_dashboard import (
    AdminDashboardAPIView,
)

from realestate.views.admin_apartment import (
    AdminApartmentListCreateAPIView,
    AdminApartmentDetailAPIView,
)


urlpatterns = [
    # =====================================================
    # Apartments - Public
    # =====================================================

    path(
        'apartments/',
        ApartmentListAPIView.as_view(),
        name='apartment-list',
    ),

    path(
        'apartments/<int:pk>/',
        ApartmentDetailAPIView.as_view(),
        name='apartment-detail',
    ),

    # =====================================================
    # Apartments - Admin
    # =====================================================

    path(
        'admin/apartments/',
        AdminApartmentListCreateAPIView.as_view(),
        name='admin-apartment-list-create',
    ),

    path(
        'admin/apartments/<int:pk>/',
        AdminApartmentDetailAPIView.as_view(),
        name='admin-apartment-detail',
    ),

    # =====================================================
    # Contracts
    # =====================================================

    path(
        'contracts/',
        ContractListAPIView.as_view(),
        name='contract-list',
    ),

    path(
        'contracts/create/',
        ContractCreateAPIView.as_view(),
        name='contract-create',
    ),

    path(
        'contracts/<int:pk>/cancel/',
        ContractCancelAPIView.as_view(),
        name='contract-cancel',
    ),

    # =====================================================
    # Authentication
    # =====================================================

    path(
        'auth/register/',
        RegisterAPIView.as_view(),
        name='register',
    ),

    # =====================================================
    # Admin Dashboard
    # =====================================================

    path(
        'admin-dashboard/',
        AdminDashboardAPIView.as_view(),
        name='admin-dashboard',
    ),
]

