from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from realestate.models import Apartment
from realestate.serializers import ApartmentListSerializer


class ApartmentListAPIView(generics.ListAPIView):
  queryset = Apartment.objects.filter(status='available').order_by(
      '-id'
  )  # Faqat bo'sh uylar
  serializer_class = ApartmentListSerializer
  permission_classes = [permissions.AllowAny]  # Hamma ko'rishi mumkin
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['room_count', 'floor', 'status']