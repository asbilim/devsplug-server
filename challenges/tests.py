from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from challenges.models import Challenge, Solution, Comment, Like, Dislike
from django.core.exceptions import ValidationError

User = get_user_model()

# Model Tests
class ChallengeModelTests(TestCase):
    def setUp(self):
        """Create test user and challenge"""
        self.user = User.objects.create_user(
            username='challengeTester',
            password='testpass123',
            email='tester@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Unique Challenge',
            description='A challenge for testing',
            content='Test challenge content',
            difficulty='easy',
            points=100
        )
        self.test_data = {
            'title': 'Unique Challenge',
            'difficulty': 'easy',
            'points': 100
        }

    def test_challenge_creation(self):
        """Test that a challenge is created with correct attributes"""
        self.assertEqual(self.challenge.title, 'Unique Challenge')
        self.assertEqual(self.challenge.points, 100)
        self.assertTrue(self.challenge.slug)
        self.current_test_response = {
            'status_code': 200,
            'data': {
                'title': self.challenge.title,
                'points': self.challenge.points,
                'slug': self.challenge.slug
            }
        }

    def test_unique_title(self):
        """Test that challenges must have unique titles"""
        with self.assertRaises(ValidationError):
            Challenge(
                title='Unique Challenge',
                description='Duplicate challenge',
                content='Duplicate content',
                difficulty='medium',
                points=150
            ).full_clean()
        self.current_test_response = {
            'status_code': 400,
            'error': 'Challenge with this title already exists'
        }

# View Tests
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

    # ... rest of your API tests ...

class SolutionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123',
            email='testuser@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test Description',
            content='Test Content',
            difficulty='easy',
            points=50
        )
        self.client.force_authenticate(user=self.user)

    def test_submit_solution(self):
        """Test submitting a solution to a challenge"""
        url = reverse('solution-list')
        data = {
            'challenge': self.challenge.id,
            'code': 'print("Hello World")',
            'language': 'python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 'print("Hello World")')
        self.assertEqual(response.data['status'], 'pending')

    def test_solution_privacy(self):
        """Test that private solutions are only visible to their owners"""
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='test code',
            language='python',
            is_private=True
        )
        
        # Owner should see their private solution
        url = reverse('solution-detail', args=[solution.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Create another user
        other_user = User.objects.create_user(
            username='other', 
            password='testpass123',
            email='other@example.com'
        )
        self.client.force_authenticate(user=other_user)
        
        # Other user should not see private solution
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SocialInteractionTests(APITestCase):
    def setUp(self):
        """Create test user, challenge, and solution for social interaction tests"""
        self.user = User.objects.create_user(
            username='social_user',
            password='testpass123',
            email='social@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Social Challenge',
            description='Test description',
            content='Test content',
            difficulty='easy',
            points=50
        )
        self.solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='print("test")',
            language='python'
        )
        self.client.force_authenticate(user=self.user)
        self.test_data = {
            'solution_id': self.solution.id
        }

    def test_like_solution(self):
        """Test that a user can like a solution"""
        url = reverse('solution-like-list', kwargs={'solution_pk': self.solution.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.current_test_response = {
            'status_code': response.status_code,
            'data': response.data
        }

    def test_comment_on_solution(self):
        """Test that a user can comment on a solution"""
        url = reverse('solution-comment-list', kwargs={'solution_pk': self.solution.id})
        data = {'content': 'Great solution!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.current_test_response = {
            'status_code': response.status_code,
            'data': response.data
        }
