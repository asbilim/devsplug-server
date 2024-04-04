from .serializer import ProblemItemSerializer,ProblemSerializer,ProblemQuizSerializer,QuizQuestionSerializer,QuizQuestionAnswerSerializer,RatingsSerializer
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Problems,ProblemItem,QuizQuestionAnswer,QuizQuestion,ProblemQuiz, Ratings
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
class ProblemsViewset(ReadOnlyModelViewSet):

    serializer_class = ProblemSerializer
    queryset = Problems.objects.all()

class ProblemItemViewset(ReadOnlyModelViewSet):

    serializer_class = ProblemItemSerializer
    queryset = ProblemItem.objects.all()
    
    @action(detail=False, methods=['post'], url_path='details')
    def get_by_slug(self, request, slug=None):
        slug = request.data.get('slug')
        queryset = self.get_queryset()
        problem_item = get_object_or_404(queryset, slug=slug)
        serializer = self.get_serializer(problem_item)
        return Response(serializer.data)
    
class QuizQuestionView(ReadOnlyModelViewSet):

    serializer_class = QuizQuestionSerializer
    queryset = QuizQuestion.objects.all()

class ProblemQuizView(ReadOnlyModelViewSet):

    serializer_class = ProblemQuizSerializer
    queryset = ProblemQuiz.objects.all()
    

    @action(detail=False, methods=['post'], url_path='details')
    def get_by_slug(self, request, slug=None):
        slug = request.data.get('slug')
        queryset = self.get_queryset()
        problem_item = get_object_or_404(queryset, slug=slug)
        serializer = self.get_serializer(problem_item)
        return Response(serializer.data)

class QuizQuestionAnswerView(ModelViewSet):

    serializer_class = QuizQuestionAnswerSerializer
    queryset = QuizQuestionAnswer.objects.all()

    
class RatingViewset(ModelViewSet):

    serializer_class = RatingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Ratings.objects.filter(parent__isnull=True)

    @action(detail=False, methods=['get', 'post'], url_path='by-problem-item/(?P<slug>[^/.]+)')
    def by_problem_item(self, request, slug=None):
        if request.method == 'GET':
            ratings = self.queryset.filter(problem_item__slug=slug)
            serializer = self.serializer_class(ratings, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
                
                problem_item = get_object_or_404(ProblemItem, slug=slug)
                
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save(user=request.user, problem_item=problem_item)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)