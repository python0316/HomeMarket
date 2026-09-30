from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from realestate.models import User


class UserAuthTestCase(APITestCase):

  def test_user_registration(self):
    url = reverse('register')
    data = {
        'username': 'newclient',
        'password': 'strongpassword123',
        'phone_number': '+998931112233',
        'passport_number': 'AB1234567',
        'address': 'Toshkent sh.',
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('username', response.data)

  def test_jwt_login(self):
    # Avval foydalanuvchi yaratamiz
    User.objects.create_user(
        username='loginclient',
        password='password123',
        phone_number='+998909998877',
    )
    url = reverse('token_obtain_pair')
    data = {'username': 'loginclient', 'password': 'password123'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)