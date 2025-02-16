from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    # Removed legacy problems field:
    # problems = ProblemSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'motivation', 'score', 'profile', 'title']

class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'score', 'profile', 'title', 'motivation']
        read_only_fields = ['id', 'username', 'profile', 'score', 'title', 'motivation']

class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = User
        fields = ['username','password','email']

class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile', 'motivation']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile': {'required': False},
            'motivation': {'required': False}
        }

    def validate_email(self, value):
        """Validate email uniqueness"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        """Validate username uniqueness"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'following', 'created_at']
        extra_kwargs = {
            'following': {'required': True}
        }

    def validate(self, data):
        if Follow.objects.filter(follower=self.context['request'].user, following=data['following']).exists():
            raise serializers.ValidationError("You are already following this user")
        return data
        