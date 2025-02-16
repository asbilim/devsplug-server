from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.models import Follow
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='authTester',
            password='testpass123',
            email='auth@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.score, 0)
        # For a new user with 0 score, title should be 'Beginner'
        self.assertEqual(self.user.title, 'Beginner')

    def test_add_points_and_title_update(self):
        self.user.add_points(600)
        self.user.refresh_from_db()
        self.assertEqual(self.user.score, 600)
        # With a score of 600, the user should have the title corresponding to threshold 500.
        self.assertEqual(self.user.title, 'Novice')
        
        self.user.add_points(500)  # Total becomes 1100
        self.user.refresh_from_db()
        self.assertEqual(self.user.title, 'Developer')  # Crosses 1000 threshold

class FollowModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='follower',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='following',
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
        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                follower=self.user1,
                following=self.user2
            ) 