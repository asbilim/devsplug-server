from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import mail
from authentication.models import Follow
from challenges.models import Challenge, Solution

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }

    def test_user_registration(self):
        url = reverse('user-create')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)  # Verify activation email was sent

    def test_user_login(self):
        # Create an active user first
        user = User.objects.create_user(**self.user_data)
        user.is_active = True
        user.save()

        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class FollowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse('follow-list')
        data = {
            'following_id': self.user2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(
            follower=self.user1,
            following=self.user2
        ).exists())

    def test_unfollow_user(self):
        # First follow the user
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        url = reverse('follow-list')
        data = {
            'following_id': self.user2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(
            follower=self.user1,
            following=self.user2
        ).exists())

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.client.force_authenticate(user=self.user1)

    def test_get_profile(self):
        url = reverse('user-detail', args=['user1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')

    def test_follow_user(self):
        url = reverse('follow-list')
        data = {'following': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_leaderboard(self):
        url = reverse('user-leaderboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class SolutionPrivacyTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.challenge = Challenge.objects.create(title='Test Challenge', points=50)
        self.solution = Solution.objects.create(
            user=self.user1, 
            challenge=self.challenge,
            code='private code',
            is_private=True
        )

    def test_private_solution_access(self):
        # User2 shouldn't see user1's private solution
        self.client.force_authenticate(user=self.user2)
        url = reverse('solution-detail', args=[self.solution.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 