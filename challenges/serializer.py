from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                               TaggitSerializer)
from django.contrib.auth import get_user_model

from .models import (
    Challenge,
    Solution,
    Comment,
    Like,
    Dislike,
    Attachment
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'profile', 'title']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'title', 'file']

class ChallengeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'content', 
                 'difficulty', 'points', 'tags', 'slug']
        read_only_fields = ['slug']

class SolutionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(queryset=Challenge.objects.all())
    
    class Meta:
        model = Solution
        fields = ['id', 'user', 'challenge', 'code', 'language', 
                 'status', 'created_at', 'is_private']
        read_only_fields = ['user', 'status']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'parent']
        read_only_fields = ['user', 'solution']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'solution']

class DislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Dislike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'solution']