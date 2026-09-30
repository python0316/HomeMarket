from rest_framework import generics, permissions
from realestate.models import Contract
from realestate.serializers import ContractCreateSerializer, ContractListSerializer


class ContractCreateAPIView(generics.CreateAPIView):
  queryset = Contract.objects.all()
  serializer_class = ContractCreateSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save()


class ContractListAPIView(generics.ListAPIView):
  serializer_class = ContractListSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    # Agar admin bo'lsa barchasini ko'rsatadi, oddiy mijoz bo'lsa faqat o'zining shartnomalarini
    if user.is_staff:
      return Contract.objects.all().order_by('-created_at')
    return Contract.objects.filter(client=user).order_by('-created_at')