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
        fields = ["username","profile","email","password","first_name","last_name"]

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
        