from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from realestate.models import (
    User,
    Apartment,
    Contract,
    PaymentPlan,
    PaymentSchedule,
    AuditLog,
)


class AdminDashboardAPIView(APIView):
    """
    HomeMarket admin dashboard statistikasi.
    Faqat staff foydalanuvchilar foydalanishi mumkin.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "users": {
                "total": User.objects.count(),
                "clients": User.objects.filter(
                    is_client=True
                ).count(),
                "staff": User.objects.filter(
                    is_staff=True
                ).count(),
            },

            "apartments": {
                "total": Apartment.objects.count(),
                "available": Apartment.objects.filter(
                    status="available"
                ).count(),
                "reserved": Apartment.objects.filter(
                    status="reserved"
                ).count(),
                "sold": Apartment.objects.filter(
                    status="sold"
                ).count(),
            },

            "contracts": {
                "total": Contract.objects.count(),
                "pending": Contract.objects.filter(
                    status="pending"
                ).count(),
                "approved": Contract.objects.filter(
                    status="approved"
                ).count(),
                "cancelled": Contract.objects.filter(
                    status="cancelled"
                ).count(),
            },

            "payments": {
                "total": PaymentSchedule.objects.count(),
                "pending": PaymentSchedule.objects.filter(
                    status="pending"
                ).count(),
                "paid": PaymentSchedule.objects.filter(
                    status="paid"
                ).count(),
                "overdue": PaymentSchedule.objects.filter(
                    status="overdue"
                ).count(),
            },

            "payment_plans": {
                "total": PaymentPlan.objects.count(),
                "active": PaymentPlan.objects.filter(
                    is_active=True
                ).count(),
                "inactive": PaymentPlan.objects.filter(
                    is_active=False
                ).count(),
            },

            "audit_logs": {
                "total": AuditLog.objects.count(),
            },
        }

        return Response(data)