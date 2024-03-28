from rest_framework import serializers
from .models import ProblemItem, ProblemQuiz, QuizQuestion, QuizQuestionAnswer, Problems, UserAnswer
from authentication.models import User

class QuizQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionAnswer
        fields = ['id', 'content', 'is_correct']

class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ['id', 'title', 'slug', 'value', 'answers']

class ProblemQuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemQuiz
        fields = ['id', 'title', 'slug', 'problem', 'questions']

class ProblemItemSerializer(serializers.ModelSerializer):
    quiz = ProblemQuizSerializer(read_only=True)

    class Meta:
        model = ProblemItem
        fields = ['id', 'title', 'slug', 'tags', 'content', 'points', 'level', 'attachments', 'quiz']

class ProblemsSerializer(serializers.ModelSerializer):
    problems = ProblemItemSerializer(many=True, read_only=True)

    class Meta:
        model = Problems
        fields = ['id', 'title', 'slug', 'tags', 'content', 'problems']

class UserAnswerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    
    selected_answer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'problem_item', 'question', 'selected_answer_id', 'is_correct']

    def create(self, validated_data):
        # Manually create the UserAnswer instance to handle the selected_answer_id
        validated_data['selected_answer'] = QuizQuestionAnswer.objects.get(id=validated_data.pop('selected_answer_id'))
        return super().create(validated_data)

    def to_representation(self, instance):
        # Customize the representation as needed, for example, include full details of the selected answer
        representation = super().to_representation(instance)
        representation['selected_answer'] = QuizQuestionAnswerSerializer(instance.selected_answer).data
        return representation
