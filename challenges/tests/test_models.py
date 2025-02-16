from django.test import TestCase
from django.contrib.auth import get_user_model
from challenges.models import Challenge, Solution, Comment, Like, Dislike
from django.core.exceptions import ValidationError

User = get_user_model()

class ChallengeModelTests(TestCase):
    def setUp(self):
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

    def test_challenge_creation(self):
        self.assertEqual(self.challenge.title, 'Unique Challenge')
        self.assertEqual(self.challenge.points, 100)
        self.assertTrue(self.challenge.slug)  # Slug should be auto-generated

    def test_unique_title(self):
        with self.assertRaises(ValidationError) as context:
            # Create another challenge with same title (case insensitive)
            challenge2 = Challenge(
                title='Unique Challenge',
                description='Duplicate challenge',
                content='Duplicate content',
                difficulty='medium',
                points=150
            )
            challenge2.full_clean()  # Should raise validation error
        self.assertIn('A challenge with this title already exists.', str(context.exception))


class SolutionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='solutionTester',
            password='testpass123',
            email='solution@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Solution Challenge',
            description='Testing solutions',
            content='Some challenge content',
            difficulty='easy',
            points=50
        )

    def test_solution_creation(self):
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code="print('Hello')",
            language="python"
        )
        self.assertEqual(solution.status, 'pending')
        self.assertEqual(solution.challenge, self.challenge)

    def test_solution_acceptance_awards_points(self):
        initial_score = self.user.score
        solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code="print('Hello World')",
            language="python"
        )
        solution.status = 'accepted'
        solution.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.score, initial_score + self.challenge.points)


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='commentTester',
            password='testpass123',
            email='comment@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Comment Challenge',
            description='Testing comments',
            content='Challenge content',
            difficulty='medium',
            points=30
        )
        self.solution = Solution.objects.create(
            user=self.user,
            challenge=self.challenge,
            code="print('Comment Test')",
            language="python"
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user,
            solution=self.solution,
            content="Great solution!"
        )
        self.assertIn("Great", comment.content)
        self.assertEqual(str(comment), f"{self.user.username}: {comment.content[:30]}")


class LikeDislikeModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='liker',
            password='testpass123',
            email='liker@example.com'
        )
        self.user2 = User.objects.create_user(
            username='disliker',
            password='testpass123',
            email='disliker@example.com'
        )
        self.challenge = Challenge.objects.create(
            title='Social Challenge',
            description='Testing likes and dislikes',
            content='Challenge content',
            difficulty='hard',
            points=80
        )
        self.solution = Solution.objects.create(
            user=self.user1,
            challenge=self.challenge,
            code="print('Social Test')",
            language="python"
        )

    def test_like_creation(self):
        like = Like.objects.create(
            user=self.user2,
            solution=self.solution
        )
        self.assertEqual(str(like), f"{self.user2.username} liked solution {self.solution.id}")

    def test_dislike_creation(self):
        dislike = Dislike.objects.create(
            user=self.user2,
            solution=self.solution
        )
        self.assertEqual(str(dislike), f"{self.user2.username} disliked solution {self.solution.id}") 