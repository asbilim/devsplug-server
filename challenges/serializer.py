from rest_framework.serializers import ModelSerializer
from .models import ProblemItem,Problems,Attachment
from .models import ProblemQuiz, QuizQuestion, QuizQuestionAnswer,Ratings,Comments,Dislikes,ProblemSolution,ProblemSolutionItem,ReportSolution,Likes
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import get_user_model
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','profile','title']
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
    

class ProblemSolutionItemSerializer(ModelSerializer):
    
    class Meta:

        model = ProblemSolutionItem
        fields  = "__all__"
        

class ProblemSolutionSerializer(ModelSerializer):

    parts = ProblemSolutionItemSerializer(many=True,required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),write_only=True,source="user")
    user = UserSerializer(read_only=True)
    problem_item = ProblemItemSerializer(read_only=True)
    class Meta:

        model = ProblemSolution
        fields = "__all__"
        extra_kwargs = {'user':{"read_only":True},'unique_code':{"read_only":True}}

    def create(self, validated_data):
        

        parts_data = validated_data.pop('parts', [])
        problem_solution = ProblemSolution.objects.create(**validated_data)

        for part_data in parts_data:
         
            item = ProblemSolutionItem.objects.create(**part_data)
            problem_solution.parts.add(item)
            problem_solution.save()
        return problem_solution

    
class CommentSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
 
    class Meta:

        model = Comments
        fields = ["id","content","user","replies","created_at","parent"]        
        extra_kwargs = {'user': {'required': False},'problem_solution': {'required': False},'replies':{"read_only":True}}

    def get_replies(self, obj):
      
        replies = Comments.objects.filter(parent=obj)
 
        return CommentSerializer(replies, many=True, context=self.context).data
class LikeSerializer(ModelSerializer):

    user = UserSerializer()
 
    class Meta:

        model = Likes
        fields = "__all__"        
        extra_kwargs = {'user': {'required': False},'problem_solution': {'required': False}}


class DisLikeSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:

        model = Dislikes
        fields = "__all__"        
        extra_kwargs = {'user': {'required': False},'problem_solution': {'required': False}}


class ReportSolutionSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:

        model = ReportSolution
        fields = "__all__"        
        extra_kwargs = {'user': {'required': False},'problem_solution': {'required': False}}