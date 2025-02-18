import shutil
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import os
from django.conf import settings
import random
import uuid
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import jwt

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

    def send_verification_email(self):
        """Send verification email with secure token"""
        token = self._generate_verification_token()
        verification_url = self._get_verification_url(token)
        
        context = {
            'user': self,
            'verification_url': verification_url,
            'expiry_hours': settings.EMAIL_VERIFICATION_TIMEOUT // 3600  # Convert seconds to hours
        }
        
        html_content = render_to_string('emails/verification_email.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            'Verify Your Devsplug Account',
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [self.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    def send_password_reset_email(self):
        """Send password reset email with secure token"""
        token = self._generate_reset_token()
        reset_url = self._get_reset_url(token)
        
        context = {
            'user': self,
            'reset_url': reset_url,
            'expiry_hours': settings.PASSWORD_RESET_TIMEOUT // 3600
        }
        
        html_content = render_to_string('emails/password_reset.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            'Reset Your Devsplug Password',
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [self.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    def _generate_verification_token(self):
        """Generate a secure JWT token for email verification"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': timezone.now() + timedelta(seconds=settings.EMAIL_VERIFICATION_TIMEOUT),
            'type': 'email_verification'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def _generate_reset_token(self):
        """Generate a secure JWT token for password reset"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': timezone.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT),
            'type': 'password_reset'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def _get_verification_url(self, token):
        """Generate the full verification URL"""
        return f"{settings.SITE_URL}/en/auth/verify-email/token/{token}"

    def _get_reset_url(self, token):
        """Generate the full password reset URL"""
        return f"{settings.SITE_URL}/en/auth/reset-password/token/{token}"

    @staticmethod
    def verify_token(token, token_type):
        """Verify a JWT token and return the user"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload['type'] != token_type:
                raise jwt.InvalidTokenError('Invalid token type')
            user = User.objects.get(id=payload['user_id'], email=payload['email'])
            return user
        except jwt.ExpiredSignatureError:
            raise ValueError('Token has expired')
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise ValueError('Invalid token')

class Follow(models.Model):
    """Model to store follow relationships between users."""
    follower = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"