from rest_framework import serializers
from .models import User,UserQuiz
from challenges.serializer import ProblemSerializer


class UserSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'motivation', 'score', 'profile', 'problems', 'title']

class LeaderSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'username', 'score', 'profile',  'title']
        extra_kwargs={'id':{'read_only':True},'username':{'read_only':True},'profile':{'read_only':True},'score':{'read_only':True},'title':{'read_only':True}}

class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = User
        fields = ['username','password','email']

class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = User
        fields = "__all__"

class UserQuizSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserQuiz
        fields = ['problem_quiz','is_complete','current_question']
        