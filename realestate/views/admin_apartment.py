from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from realestate.models import Apartment
from realestate.serializers.apartment import ApartmentListSerializer


class AdminApartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Apartment.objects.all().order_by('-created_at')
    serializer_class = ApartmentListSerializer
    permission_classes = [permissions.IsAdminUser]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        'status',
        'room_count',
        'property_type',
        'district',
        'city',
        'renovation',
    ]

    search_fields = [
        'title',
        'address',
        'district',
        'city',
    ]

    ordering_fields = [
        'created_at',
        'updated_at',
        'total_price',
        'square_meters',
        'floor',
    ]

    ordering = ['-created_at']


class AdminApartmentDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentListSerializer
    permission_classes = [permissions.IsAdminUser]

