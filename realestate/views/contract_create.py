from rest_framework import generics, permissions
from realestate.models import Contract
from realestate.serializers import ContractCreateSerializer


class ContractCreateAPIView(generics.CreateAPIView):
  queryset = Contract.objects.all()
  serializer_class = ContractCreateSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save()