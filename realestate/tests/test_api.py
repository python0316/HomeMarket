from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from realestate.models import User, Apartment, PaymentPlan


class ContractAPITestCase(APITestCase):

  def setUp(self):
    # Test uchun mijoz yaratamiz
    self.client_user = User.objects.create_user(
        username='testclient',
        password='password123',
        phone_number='+998901234567',
        is_client=True,
    )
    # Kvartira yaratamiz
    self.apartment = Apartment.objects.create(
        room_count=3,
        square_meters=80.0,
        floor=5,
        total_price=1000000000.00,  # 1 mlrd so'm
        status='available',
    )
    # To'lov rejasini yaratamiz (24 oy, min 30% boshlang'ich)
    self.payment_plan = PaymentPlan.objects.create(
        duration_months=24, min_initial_payment_percent=30.0, is_active=True
    )
    self.url = reverse('contract-create')

  def test_create_contract_success(self):
    # Tizimga kiramiz (JWT yoki Token orqali, hozircha APIClient login)
    self.client.force_authenticate(user=self.client_user)

    data = {
        'apartment_id': self.apartment.id,
        'payment_plan_id': self.payment_plan.id,
        'initial_payment': 300000000.00,  # 300 mln (30%)
    }

    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('contract_number', response.data)
    self.assertEqual(float(response.data['monthly_payment']), 29166666.67)