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
        self.user = User.objects.create_user(
            username='challengeAPI',
            password='testpass123',
            email='challengeapi@example.com'
        )
        self.challenge = Challenge.objects.create(
            title="API Challenge",
            description="Testing challenge",
            content="Challenge content",
            difficulty="easy",
            points=75
        )
        self.client.force_authenticate(user=self.user)

    def test_challenge_list(self):
        url = reverse('challenge-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the created challenge is in the list.
        self.assertTrue(any(ch['title'] == "API Challenge" for ch in response.data))

    def test_submit_solution(self):
        url = reverse('challenge-submit-solution', kwargs={'slug': self.challenge.slug})
        data = {
            "code": "print('Test solution')",
            "language": "python"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "print('Test solution')")


class SolutionNestedAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nestedAPI',
            password='testpass123',
            email='nested@example.com'
        )
        self.challenge = Challenge.objects.create(
            title="Nested Challenge",
            description="Nested endpoints",
            content="Content for nested test",
            difficulty="medium",
            points=90
        )
        self.solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code="print('Nested test')",
            language="python"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_comment_for_solution(self):
        url = reverse('solution-comment-list', kwargs={'solution_pk': self.solution.id})
        data = {
            "content": "Nice solution!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("content"), "Nice solution!")

    def test_like_solution(self):
        url = reverse('solution-like-list', kwargs={'solution_pk': self.solution.id})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dislike_solution(self):
        url = reverse('solution-dislike-list', kwargs={'solution_pk': self.solution.id})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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