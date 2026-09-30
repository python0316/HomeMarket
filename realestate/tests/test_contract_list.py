from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from realestate.models import User, Apartment, PaymentPlan, Contract


class ContractListAPITestCase(APITestCase):

  def setUp(self):
    # Mijoz va admin foydalanuvchilarni yaratamiz
    self.client_user = User.objects.create_user(
        username='client1',
        password='password123',
        phone_number='+998901112233',
        is_client=True,
    )
    self.admin_user = User.objects.create_superuser(
        username='admin1', password='password123', phone_number='+998909998877'
    )

    # Kvartira va to'lov rejasi
    self.apartment = Apartment.objects.create(
        room_count=2,
        square_meters=60.0,
        floor=2,
        total_price=700000000.00,
        status='reserved',
    )
    self.payment_plan = PaymentPlan.objects.create(
        duration_months=12, min_initial_payment_percent=30.0, is_active=True
    )

    # Mijoz nomidan shartnoma yaratib qo'yamiz
    self.contract = Contract.objects.create(
        client=self.client_user,
        apartment=self.apartment,
        payment_plan=self.payment_plan,
        initial_payment=210000000.00,
        monthly_payment=40833333.33,
        remaining_amount=490000000.00,
        contract_number='CON-12345',
        status='pending',
    )
    self.url = reverse('contract-list')

  def test_client_can_see_only_own_contracts(self):
    self.client.force_authenticate(user=self.client_user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Mijoz faqat o'zining 1 ta shartnomasini ko'rishi kerak
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['contract_number'], 'CON-12345')

  def test_admin_can_see_all_contracts(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Admin barcha shartnomalarni ko'ra oladi
    self.assertGreaterEqual(len(response.data), 1)