from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import mail
from authentication.models import Follow, VerificationCode, ResetCode
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from PIL import Image
import io

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

class UserProfileTests(APITestCase):
    def setUp(self):
        """Set up test user and authentication"""
        self.user = User.objects.create_user(
            username='profiletest',
            password='testpass123',
            email='profile@test.com'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_update_profile(self):
        """Test updating user profile information"""
        url = reverse('user-update', kwargs={'pk': self.user.id})
        
        # Create a proper test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        image_data = SimpleUploadedFile(
            "test_profile.jpg",
            image_io.getvalue(),
            content_type="image/jpeg"
        )
        
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'updated@test.com',
            'profile': image_data,
            'motivation': 'Test motivation'
        }
        
        response = self.client.patch(
            url, 
            data,
            format='multipart',
            HTTP_CONTENT_TYPE='multipart/form-data'
        )
        
        print("Response data:", response.data)  # Add this for debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify updates
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.email, 'updated@test.com')
        self.assertEqual(self.user.motivation, 'Test motivation')
        self.assertTrue(self.user.profile)

class AccountActivationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-create')
        self.activate_url = reverse('user-activate')
        self.claim_code_url = reverse('user-code-claim')
        self.user_data = {
            'username': 'activationtest',
            'password': 'testpass123',
            'email': 'info@paullilian.dev'
        }

    def test_registration_and_activation_flow(self):
        """Test complete registration and activation flow"""
        # 1. Register user
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. Verify user is created but inactive
        user = User.objects.get(username=self.user_data['username'])
        self.assertFalse(user.is_active)
        
        # 3. Verify verification code was created
        verification = VerificationCode.objects.filter(user=user).first()
        self.assertIsNotNone(verification)
        
        # 4. Verify email was sent and check content
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], self.user_data['email'])
        self.assertIn('verification code', email.subject.lower())
        self.assertIn(verification.code, email.body)
        print("\nVerification Email:", email.subject)
        print("To:", email.to)
        print("Content:", email.body)
        
        # 5. Activate account
        activation_data = {
            'code': verification.code,
            'email': self.user_data['email']
        }
        response = self.client.post(self.activate_url, activation_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        
        # 6. Verify user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='resettest',
            password='oldpass123',
            email='info@paullilian.dev'
        )
        self.apply_url = reverse('user-password-apply')
        self.verify_url = reverse('user-password-verify')
        self.change_url = reverse('user-password-change')

    def test_password_reset_flow(self):
        """Test complete password reset flow"""
        # 1. Request password reset
        response = self.client.post(self.apply_url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 2. Verify reset code was created
        reset_code = ResetCode.objects.filter(user=self.user).first()
        self.assertIsNotNone(reset_code)
        
        # 3. Verify email was sent and check content
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], self.user.email)
        self.assertIn('verification code', email.subject.lower())
        self.assertIn(reset_code.code, email.body)
        print("\nReset Email:", email.subject)
        print("To:", email.to)
        print("Content:", email.body)
        
        # 4. Verify reset code
        verify_data = {
            'code': reset_code.code,
            'email': self.user.email
        }
        response = self.client.post(self.verify_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Change password
        change_data = {
            'code': reset_code.code,
            'email': self.user.email,
            'password': 'newpass123'
        }
        response = self.client.post(self.change_url, change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 6. Verify new password works
        login_response = self.client.post(reverse('token_obtain_pair'), {
            'username': self.user.username,
            'password': 'newpass123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
