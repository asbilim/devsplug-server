from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                               TaggitSerializer)

class ChallengeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'content', 
                 'difficulty', 'points', 'tags', 'slug']
        read_only_fields = ['slug']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['user'] 

class LikeSerializer(serializers.ModelSerializer):
    solution = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'created_at', 'solution']
        read_only_fields = ['user', 'solution']

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'challenge', 'code', 'language', 'status', 'created_at']
        read_only_fields = ['user', 'status'] 