from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_USER_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PubliUserApiTests(TestCase):
    '''Test user api (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''Test creating user with valid payload is successful'''
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''Test creating a user that already exists fails'''

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test that user password must be more than 5 characters'''

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pass',
            'name': 'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''Test that a token is created for a user'''

        payload = {
            'email': 'user@test.com',
            'password': 'Password123',
            'name': 'Test user'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid(self):
        '''Test that no token is created when invalid data is submitted'''
        create_user(email='testuser@user.com', password='Password123')

        payload = {
            'email': 'testuser@user.com',
            'password': 'wrongpassword'
        }

        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_no_user(self):
        """Test that no token is created for a non-existing user"""
        payload = { 'email': 'test@user.com', 'password': 'Password123' }
        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_no_password(self):
        """Test that no token is created when no password is provided"""
        payload = { 'email': 'test@testab.com', 'password': '' }
        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)