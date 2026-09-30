from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from realestate.models import Apartment


class ApartmentAPITestCase(APITestCase):

  def setUp(self):
    Apartment.objects.create(
        room_count=2,
        square_meters=55.0,
        floor=3,
        total_price=600000000.00,
        status='available',
    )
    Apartment.objects.create(
        room_count=3,
        square_meters=85.0,
        floor=5,
        total_price=900000000.00,
        status='available',
    )
    self.url = reverse('apartment-list')

  def test_get_apartment_list(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

  def test_filter_apartments_by_room(self):
    response = self.client.get(self.url, {'room_count': 2})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['room_count'], 2)