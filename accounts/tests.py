from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def test_login_and_me(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='P@ssw0rd123',
        )

        login_response = self.client.post(
            reverse('login'),
            {'email': 'test@example.com', 'password': 'P@ssw0rd123'},
            format='json',
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('access', login_response.data)

        me_response = self.client.get(reverse('me'), HTTP_AUTHORIZATION='Bearer ' + login_response.data['access'])
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data['email'], 'test@example.com')
