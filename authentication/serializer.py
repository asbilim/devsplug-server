from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Follow
from challenges.serializer import ProblemSerializer


class UserSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'motivation', 'score', 'profile', 'problems', 'title']

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
        fields = ["username","profile","email","password","first_name","last_name"]

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["follower"]
        