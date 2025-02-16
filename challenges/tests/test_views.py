from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from challenges.models import Challenge, Solution, Comment, Like
import json

User = get_user_model()

class ChallengeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test Description',
            content='Test Content',
            difficulty='easy',
            points=50
        )

    def test_list_challenges(self):
        url = reverse('challenge-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_challenge(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('challenge-list')
        data = {
            'title': 'New Challenge',
            'description': 'New Description',
            'content': 'New Content',
            'difficulty': 'medium',
            'points': 100,
            'tags': ['python', 'testing']
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Add this to see validation errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Challenge.objects.count(), 2)

class SolutionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test Description',
            content='Test Content',
            difficulty='easy',
            points=50
        )

    def test_submit_solution(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('solution-list')
        data = {
            'challenge': self.challenge.id,
            'code': 'print("Hello World")',
            'language': 'python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

    def test_solution_acceptance(self):
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='test code',
            language='python'
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('solution-detail', args=[solution.id])
        data = {'status': 'accepted'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.score, 50)

class SocialInteractionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test description',
            content='Test content',
            difficulty='easy'
        )
        self.solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='def solution(): pass',
            language='python'
        )
        self.client.force_authenticate(user=self.user)

    def test_add_comment(self):
        url = reverse('solution-comment-list', kwargs={'solution_pk': self.solution.id})
        data = {
            'content': 'Great solution!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content='Great solution!').exists())

    def test_like_solution(self):
        url = reverse('solution-like-list', kwargs={'solution_pk': self.solution.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, solution=self.solution).exists()) 