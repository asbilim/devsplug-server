from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import mail
from authentication.models import Follow, VerificationCode
from django.db import IntegrityError

User = get_user_model()

# Model Tests
class UserModelTests(TestCase):
    def setUp(self):
        """Create a test user with basic attributes"""
        self.user = User.objects.create_user(
            username='authTester',
            password='testpass123',
            email='auth@example.com'
        )
        self.test_data = {
            'username': 'authTester',
            'email': 'auth@example.com'
        }

    def test_user_creation(self):
        """Test that a user is created with correct default values"""
        self.assertEqual(self.user.score, 0)
        self.assertEqual(self.user.title, 'Beginner')
        self.current_test_response = {
            'status_code': 200,
            'data': {
                'score': self.user.score,
                'title': self.user.title
            }
        }

    def test_add_points_and_title_update(self):
        """Test that user title updates correctly when points are added"""
        self.user.add_points(600)
        self.user.refresh_from_db()
        self.assertEqual(self.user.score, 600)
        self.assertEqual(self.user.title, 'Novice')
        self.current_test_response = {
            'status_code': 200,
            'data': {
                'score': self.user.score,
                'title': self.user.title
            }
        }

# API Tests
class AuthenticationTests(APITestCase):
    def setUp(self):
        """Prepare test client and user data"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.test_data = self.user_data

    def test_user_registration(self):
        """Test user registration with valid credentials"""
        url = reverse('user-create')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.current_test_response = {
            'status_code': response.status_code,
            'data': response.data
        }

    def test_user_login(self):
        """Test user login with valid credentials"""
        user = User.objects.create_user(**self.user_data)
        user.is_active = True
        user.save()
        
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.current_test_response = {
            'status_code': response.status_code,
            'data': {'access_token': 'Received'}
        }

class FollowTests(APITestCase):
    def setUp(self):
        """Create users for follow testing"""
        self.user1 = User.objects.create_user(
            username='follower',
            password='testpass123',
            email='follower@test.com'
        )
        self.user2 = User.objects.create_user(
            username='following',
            password='testpass123',
            email='following@test.com'
        )
        self.client.force_authenticate(user=self.user1)
        self.test_data = {'following': self.user2.id}

    def test_follow_user(self):
        """Test that a user can successfully follow another user"""
        url = reverse('follow-list')
        response = self.client.post(url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Store response for test runner
        self.current_test_response = {
            'status_code': response.status_code,
            'data': response.data
        }

    def test_unique_follow(self):
        """Test that a user cannot follow another user twice"""
        url = reverse('follow-list')
        # First follow
        self.client.post(url, self.test_data)
        # Try duplicate
        response = self.client.post(url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already following', str(response.content))
        # Store response for test runner
        self.current_test_response = {
            'status_code': response.status_code,
            'error': str(response.content)
        }
