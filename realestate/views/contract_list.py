from rest_framework import generics, permissions
from realestate.models import Contract
from realestate.serializers import ContractListSerializer


class ContractListAPIView(generics.ListAPIView):
  serializer_class = ContractListSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Contract.objects.all().order_by('-created_at')
    return Contract.objects.filter(client=user).order_by('-created_at')