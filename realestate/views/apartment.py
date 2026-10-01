from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from realestate.models import Apartment
from realestate.serializers import ApartmentListSerializer


class ApartmentListAPIView(generics.ListAPIView):
    queryset = Apartment.objects.filter(
        status='available'
    ).order_by('-created_at')

    serializer_class = ApartmentListSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'room_count',
        'floor',
        'status',
        'district',
        'renovation',
        'property_type',
        'city',
    ]


class ApartmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Apartment.objects.filter(
        status='available'
    )

    serializer_class = ApartmentListSerializer

    permission_classes = [
        permissions.AllowAny
    ]