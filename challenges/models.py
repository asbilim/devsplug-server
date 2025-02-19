from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", default="fa-code")
    order = models.IntegerField(default=0, help_text="Order in which category appears")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def get_stats(self):
        challenges = self.challenges.all()
        return {
            'total_challenges': challenges.count(),
            'avg_difficulty': challenges.aggregate(Avg('points'))['points__avg'] or 0,
            'total_solutions': Solution.objects.filter(challenge__in=challenges).count()
        }

class Attachment(models.Model):
    title = models.TextField(unique=True)
    file = models.FileField(upload_to="attachments/")
    description = models.TextField(blank=True, help_text="Optional description of the attachment")
    file_type = models.CharField(max_length=50, help_text="Type of file (e.g., 'dataset', 'template', 'test_case')")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Challenge(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ]
    )
    points = models.IntegerField()
    tags = TaggableManager()
    attachments = models.ManyToManyField(Attachment, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='challenges')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, 
                                         help_text="Challenges that should be completed before this one")
    estimated_time = models.IntegerField(default=30, help_text="Estimated time in minutes to complete")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_completion_rate(self):
        total_attempts = Solution.objects.filter(challenge=self).count()
        if total_attempts == 0:
            return 0
        successful_attempts = Solution.objects.filter(challenge=self, status='accepted').count()
        return (successful_attempts / total_attempts) * 100

    def get_stats(self):
        solutions = Solution.objects.filter(challenge=self)
        return {
            'total_attempts': solutions.count(),
            'successful_attempts': solutions.filter(status='accepted').count(),
            'total_likes': Like.objects.filter(solution__challenge=self).count(),
            'completion_rate': self.get_completion_rate()
        }

class Solution(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.TextField()
    documentation = models.TextField(blank=True, help_text="Documentation for the solution")
    language = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s solution for {self.challenge.title}"

class Comment(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

class Like(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="challenge_likes")
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'solution')

    def __str__(self):
        return f"{self.user.username} liked solution {self.solution.id}"

class Dislike(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="challenge_dislikes")
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'solution')

    def __str__(self):
        return f"{self.user.username} disliked solution {self.solution.id}"

class UserChallenge(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='subscribed_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='subscribed_users')
    is_subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    last_attempted_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.challenge.title}"

    def get_attempts(self):
        return Solution.objects.filter(user=self.user, challenge=self.challenge).count()

    def get_successful_attempts(self):
        return Solution.objects.filter(
            user=self.user, 
            challenge=self.challenge,
            status='accepted'
        ).count()
    