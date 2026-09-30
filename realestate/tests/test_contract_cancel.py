from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from realestate.models import Apartment, Contract, PaymentPlan, User


class ContractCancelAPITestCase(APITestCase):

  def setUp(self):
    self.client_user = User.objects.create_user(
        username='client_cancel',
        password='password123',
        phone_number='+998901112233',
    )
    self.apartment = Apartment.objects.create(
        room_count=1,
        square_meters=40.0,
        floor=1,
        total_price=500000000.00,
        status='reserved',
    )
    self.payment_plan = PaymentPlan.objects.create(
        duration_months=12, min_initial_payment_percent=20.0, is_active=True
    )
    self.contract = Contract.objects.create(
        client=self.client_user,
        apartment=self.apartment,
        payment_plan=self.payment_plan,
        initial_payment=100000000.00,
        monthly_payment=33333333.33,
        remaining_amount=400000000.00,
        contract_number='CON-CANCEL-1',
        status='pending',
    )
    self.url = reverse('contract-cancel', kwargs={'pk': self.contract.pk})

  def test_cancel_contract(self):
    self.client.force_authenticate(user=self.client_user)
    response = self.client.post(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Shartnoma statusi cancelled bo'lganini tekshiramiz
    self.contract.refresh_from_db()
    self.assertEqual(self.contract.status, 'cancelled')

    # Kvartira yana available bo'lganini tekshiramiz
    self.apartment.refresh_from_db()
    self.assertEqual(self.apartment.status, 'available')