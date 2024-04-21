from .serializer import ProblemItemSerializer,ProblemSerializer,ProblemQuizSerializer,QuizQuestionSerializer,QuizQuestionAnswerSerializer,RatingsSerializer,ProblemSolutionSerializer,CommentSerializer,LikeSerializer,DisLikeSerializer,ReportSolutionSerializer
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Comments, Dislikes, Likes, ProblemSolution, Problems,ProblemItem,QuizQuestionAnswer,QuizQuestion,ProblemQuiz, Ratings, ReportSolution
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
                


class ProblemSolutionView(ModelViewSet):

    serializer_class = ProblemSolutionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProblemSolution.objects.all()


    @action(detail=False, methods=['post'], url_path='by-problem-item/(?P<slug>[^/.]+)')
    def add_solution(self, request, slug=None):
        
        complete_datas = request.data.copy()
        complete_datas['user_id'] = request.user.id
        
        try:
            problem_item = get_object_or_404(ProblemItem, slug=complete_datas['problem_item'])
            complete_datas['problem_item'] = problem_item.id
            serializer = self.serializer_class(data=complete_datas, context={'request': request})

            if serializer.is_valid():
                serializer.save(user=request.user, problem_item=problem_item)
                return Response({"content":"your submission was accepted , you can view it in the submission section","status":"success"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"content":"you submitted a solution for this challenge already","status":"error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"You submitted a solution already","status":"error"})



   

class CommentView(ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comments.objects.filter(parent__isnull=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    @action(detail=False, methods=['get'], url_path='by-problem-item/(?P<uid>[^/.]+)')
    def get_views(self, request, uid=None):
        
        
        if uid is None :
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})

        try:
            likes =  Comments.objects.filter(problem_solution__unique_code=uid)
            amount = len(likes) if len(likes) <=9 else "9+"
            serializer = self.get_serializer(likes, many=True)
         
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})


        return Response(status=status.HTTP_200_OK,data={"status":"success","likes":serializer.data,"number":amount})

    

    @action(detail=False, methods=['get', 'post'], url_path='content/by-problem-item/(?P<slug>[^/.]+)')
    def by_problem_item(self, request, slug=None):
        if request.method == 'GET':
            ratings = self.queryset.filter(problem_solution__unique_code=slug)
            serializer = self.serializer_class(ratings, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
                
                problem_item = get_object_or_404(ProblemSolution, unique_code=slug)
                
                serializer = self.serializer_class(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save(user=request.user, problem_solution=problem_item)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeView(ModelViewSet):

    serializer_class = LikeSerializer
    queryset = Likes.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def create(self,request):

        user = request.user
        unique_code = request.data.get('unique_code')
        try:
            problem_solution = ProblemSolution.objects.filter(unique_code=unique_code).get()
            try:
                like = Likes.objects.filter(problem_solution=problem_solution,user=user).get()
                print(like)
                like.delete()
                problem_solution.user.score-=10
                problem_solution.user.save()
                return Response(status=status.HTTP_200_OK,data={"status":"success","content":"like was removed successfully"})

            except Likes.DoesNotExist:
                Likes.objects.create(user=user,problem_solution=problem_solution)
                return Response(status=status.HTTP_200_OK,data={"status":"success","content":"like was added successfully"})
            
            except Exception as e:
                print(e)

        except Exception as e:

            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid code","status":"error"})
        
        return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Something went wrong , it is not your fault","status":"error"})






    @action(detail=False, methods=['get'], url_path='by-problem-item/(?P<uid>[^/.]+)')
    def get_views(self, request, uid=None):
        
        
        if uid is None :
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})

        try:
            likes =  Likes.objects.filter(problem_solution__unique_code=uid)
            amount = len(likes) if len(likes) <=9 else "9+"
            serializer = self.get_serializer(likes, many=True)
         
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})


      
        return Response(status=status.HTTP_200_OK,data={"status":"success","likes":serializer.data,"number":amount})


class DisLikeView(ModelViewSet):

    serializer_class = DisLikeSerializer
    queryset = Dislikes.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self,request):

        user = request.user
        unique_code = request.data.get('unique_code')
        try:
            problem_solution = ProblemSolution.objects.filter(unique_code=unique_code).get()
            try:
                like = Dislikes.objects.filter(problem_solution=problem_solution,user=user).get()
                print(like)
                like.delete()
                problem_solution.user.score-=10
                problem_solution.user.save()
                return Response(status=status.HTTP_200_OK,data={"status":"success","content":"dislike was removed successfully"})

            except Dislikes.DoesNotExist:
                Dislikes.objects.create(user=user,problem_solution=problem_solution)
                return Response(status=status.HTTP_200_OK,data={"status":"success","content":"dislike was added successfully"})
            
            except Exception as e:
                print(e)

        except Exception as e:

            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid code","status":"error"})
        
        return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Something went wrong , it is not your fault","status":"error"})


    @action(detail=False, methods=['get'], url_path='by-problem-item/(?P<uid>[^/.]+)')
    def get_dislikes(self, request, uid=None):
        
        
        if uid is None :
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})

        try:
            likes =  Dislikes.objects.filter(problem_solution__unique_code=uid)
            amount = len(likes) if len(likes) <=9 else "9+"
            serializer = self.get_serializer(likes, many=True)
           
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"content":"Please provide a valid slug","status":"error"})



        return Response(status=status.HTTP_200_OK,data={"status":"success","dislikes":serializer.data,"number":amount})

class ReportView(ModelViewSet):

    serializer_class = ReportSolutionSerializer
    queryset = ReportSolution.objects.all()
    permission_classes = [permissions.IsAuthenticated]