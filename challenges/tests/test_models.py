from django.test import TestCase
from django.contrib.auth import get_user_model
from challenges.models import Challenge, Solution, Comment, Like, Dislike
from django.core.exceptions import ValidationError

User = get_user_model()

class ChallengeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test description',
            content='Test content',
            difficulty='easy',
            points=50
        )

    def test_challenge_creation(self):
        self.assertEqual(self.challenge.title, 'Test Challenge')
        self.assertEqual(self.challenge.points, 50)
        self.assertTrue(self.challenge.slug)  # Verify slug was created

    def test_unique_title(self):
        with self.assertRaises(ValidationError):
            Challenge.objects.create(
                title='Test Challenge',  # Same title as existing challenge
                description='Another description',
                content='Another content',
                difficulty='medium'
            )

class SolutionModelTests(TestCase):
    def setUp(self):
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

    def test_solution_creation(self):
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='def solution(): pass',
            language='python',
            documentation='Test documentation'
        )
        self.assertEqual(solution.status, 'pending')
        self.assertEqual(solution.user.score, 0)  # No points awarded yet

    def test_solution_acceptance(self):
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='def solution(): pass',
            language='python'
        )
        solution.status = 'accepted'
        solution.save()
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.score, 50)  # Points should be awarded 