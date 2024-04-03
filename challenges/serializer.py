from rest_framework.serializers import ModelSerializer
from .models import ProblemItem,Problems,Attachment
from .models import ProblemQuiz, QuizQuestion, QuizQuestionAnswer

class AttachmentSerializer(ModelSerializer):

    class Meta:

        model = Attachment
        fields =  ['title','file']
class ProblemItemSerializer(ModelSerializer):

    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta:

        fields = "__all__"
        model = ProblemItem

class ProblemSerializer(ModelSerializer):

    problems = ProblemItemSerializer(many=True,read_only=True)
    class Meta:

        fields = "__all__"
        model = Problems


class QuizQuestionAnswerSerializer(ModelSerializer):
    class Meta:
        model = QuizQuestionAnswer
        fields = ['id', 'content', 'is_correct']

class QuizQuestionSerializer(ModelSerializer):
    answers = QuizQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ['id', 'title', 'slug', 'value', 'answers']

class ProblemQuizSerializer(ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProblemQuiz
        fields = ['id', 'title', 'slug', 'problem', 'questions']
