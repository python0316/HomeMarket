from django.test import TestCase
from realestate.models import Apartment


class ApartmentModelTest(TestCase):

  def setUp(self):
    self.apartment = Apartment.objects.create(
        room_count=2,
        square_meters=65.5,
        floor=4,
        total_price=800000000.00,
        status='available',
    )

  def test_apartment_str(self):
    expected_str = (
        f"{self.apartment.room_count}-xona, {self.apartment.square_meters} m²"
        f" - {self.apartment.total_price} so'm"
    )
    self.assertEqual(str(self.apartment), expected_str)