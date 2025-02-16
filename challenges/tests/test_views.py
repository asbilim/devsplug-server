from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from challenges.models import Challenge, Solution, Comment, Like
import json

User = get_user_model()

class ChallengeViewTests(TestCase):
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
            difficulty='easy',
            points=50
        )
        self.client.force_authenticate(user=self.user)

    def test_list_challenges(self):
        response = self.client.get(reverse('challenge-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_submit_solution(self):
        url = reverse('challenge-submit-solution', kwargs={'pk': self.challenge.pk})
        data = {
            'code': 'def solution(): return True',
            'language': 'python',
            'documentation': 'Test documentation'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Solution.objects.filter(user=self.user, challenge=self.challenge).exists())

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
        url = reverse('comment-list')
        data = {
            'content': 'Great solution!',
            'solution': self.solution.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content='Great solution!').exists())

    def test_like_solution(self):
        url = reverse('like-list')
        data = {
            'solution': self.solution.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, solution=self.solution).exists()) 