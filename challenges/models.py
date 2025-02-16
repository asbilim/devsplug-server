from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError

class Attachment(models.Model):
    title = models.TextField(unique=True)
    file = models.FileField(upload_to="attachments/")

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Solution(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.TextField()
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
    