from rest_framework.serializers import ModelSerializer
from .models import ProblemItem,Problems,Attachment
from .models import ProblemQuiz, QuizQuestion, QuizQuestionAnswer,Ratings
from rest_framework import serializers
from authentication.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','profile']
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

class RatingsSerializer(ModelSerializer):

    replies = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    class Meta:
        model = Ratings
        fields = ['id','score','message','user','parent','replies',"created_at"]
        extra_kwargs = {'user': {'required': False},'replies':{"read_only":True}}

    def get_replies(self, obj):
      
        replies = Ratings.objects.filter(parent=obj)
 
        return RatingsSerializer(replies, many=True, context=self.context).data