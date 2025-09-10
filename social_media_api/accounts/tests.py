from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            bio='Test bio'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.bio, 'Test bio')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_followers_count(self):
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        user2.followers.add(self.user)
        self.assertEqual(self.user.following_count, 1)
        self.assertEqual(user2.followers_count, 1)


class UserRegistrationAPITest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'bio': 'New user bio'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue('user' in response.data)

    def test_user_registration_password_mismatch(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            bio='Test bio'
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_profile(self):
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        url = reverse('update_profile')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'first_name': 'Updated',
            'bio': 'Updated bio'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.bio, 'Updated bio')

