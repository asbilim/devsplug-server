from rest_framework import serializers
from .models import User
from challenges.serializer import ProblemsSerializer

class UserSerializer(serializers.ModelSerializer):
    problems = ProblemsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'motivation', 'score', 'profile', 'problems', 'title']
