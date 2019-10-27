from django.test import TestCase
from django.urls import reverse
from users.tests.factories import UserFactory
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler


class JWTAuthTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_login_success(self):
        url = reverse('jwt-auth')
        credentials = {'email': self.user.email, 'password': 'password'}
        resp = self.client.post(url, data=credentials, content_type='application/json')
        assert resp.status_code == status.HTTP_200_OK, resp.data
        assert resp.data['token'], resp.data

    def test_login_failed(self):
        url = reverse('jwt-auth')
        credentials = {'email': self.user.email, 'password': 'wrong_password'}
        resp = self.client.post(url, data=credentials, content_type='application/json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST, resp.data

    def test_permission_allowed(self):
        url = reverse('jwt-auth')
        credentials = {'email': self.user.email, 'password': 'password'}
        resp = self.client.post(url, data=credentials, content_type='application/json')
        token = resp.data['token']

        url = reverse('user_list')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        resp = self.client.get(url, **headers)
        assert resp.status_code == status.HTTP_200_OK, resp.data

    def test_permission_denied(self):
        url = reverse('user_list')
        token = "bad token"
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        resp = self.client.get(url, **headers)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED, resp.data

    def test_payload_contains_user_data(self):
        url = reverse('jwt-auth')
        credentials = {'email': self.user.email, 'password': 'password'}
        resp = self.client.post(url, data=credentials, content_type='application/json')
        assert resp.status_code == status.HTTP_200_OK, resp.data
        token = resp.data['token']
        payload = jwt_decode_handler(token)
        assert payload['first_name'] == self.user.first_name
        assert payload['last_name'] == self.user.last_name
        assert payload['email'] == self.user.email
        assert payload['is_staff'] == self.user.is_staff
