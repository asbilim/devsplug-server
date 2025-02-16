import shutil
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import os
from django.conf import settings
import random

class User(AbstractUser):
    """Simplified user model with better point management"""
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=50, blank=True)
    motivation = models.TextField(null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    
    TITLES = {
        0: 'Beginner',
        500: 'Novice',
        1000: 'Developer',
        2500: 'Engineer',
        4000: 'Architect',
        6000: 'Master',
        10000: 'Expert',
        15000: 'Legend'
    }

    def add_points(self, points):
        """Safely add points and update title"""
        self.score += points
        self._update_title()
        self.save()

    def _update_title(self):
        """Update user title based on score"""
        for threshold, title in sorted(self.TITLES.items()):
            if self.score >= threshold:
                self.title = title

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self._update_title()
        print(f"Setting title to: {self.title}")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-score','username')

class VerificationCode(models.Model):

    code = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):

        return f"otp code for {self.user}"
    
    def generate_code(self):

        code = "".join([str(random.randint(0,9)) for i in range(9)])
        self.code = code
        self.save()
        return code
    
class ResetCode(models.Model):

    code = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE,null=True,blank=True)
    can_reset = models.BooleanField(default=False)


    def generate_code(self):

        code = "".join([str(random.randint(0,9)) for i in range(9)])
        self.code = code
        self.save()
        return code
    
    def __str__(self):

        return f"reset code for {self.user}"

class Follow(models.Model):
    """Model to store follow relationships between users."""
    follower = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"