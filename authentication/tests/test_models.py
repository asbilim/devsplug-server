from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.models import Follow
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.score, 0)
        self.assertEqual(self.user.title, 'Beginner')

    def test_add_points(self):
        self.user.add_points(500)
        self.assertEqual(self.user.score, 500)
        self.assertEqual(self.user.title, 'Novice')

        self.user.add_points(600)  # Total: 1100
        self.assertEqual(self.user.title, 'Developer')

class FollowModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )

    def test_follow_creation(self):
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        self.assertTrue(Follow.objects.filter(
            follower=self.user1,
            following=self.user2
        ).exists())

    def test_unique_follow(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        # Try to create duplicate follow
        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                follower=self.user1,
                following=self.user2
            ) 