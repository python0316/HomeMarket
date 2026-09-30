from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from realestate.models import Contract


class ContractCancelAPIView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, pk):
    try:
      contract = Contract.objects.get(pk=pk)
    except Contract.DoesNotExist:
      return Response(
          {'error': 'Shartnoma topilmadi.'}, status=status.HTTP_404_NOT_FOUND
      )

    if not request.user.is_staff and contract.client != request.user:
      return Response(
          {'error': 'Sizda bu amalni bajarish huquqi yo‘q.'},
          status=status.HTTP_403_FORBIDDEN,
      )

    if contract.status == 'cancelled':
      return Response(
          {'error': 'Bu shartnoma allaqachon bekor qilingan.'},
          status=status.HTTP_400_BAD_REQUEST,
      )

    contract.status = 'cancelled'
    contract.save()

    apartment = contract.apartment
    apartment.status = 'available'
    apartment.save()

    return Response(
        {'message': 'Shartnoma muvaffaqiyatli bekor qilindi va kvartira bo‘shatildi.'},
        status=status.HTTP_200_OK,
    )