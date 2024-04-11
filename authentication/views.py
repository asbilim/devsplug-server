from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import permissions,status
from .serializer import UserCreateSerializer,UserUpdateSerializer, UserQuizSerializer,LeaderSerializer
from rest_framework.response import Response
from .models import Problems,UserQuiz,UserQuestionAttempt
from challenges.models import ProblemQuiz,UserAnswer,QuizQuestion,ProblemItem,QuizQuestionAnswer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
from .models import User
import json

class LeaderView(viewsets.ReadOnlyModelViewSet):

    serializer_class = LeaderSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'], url_path='by-username/(?P<username>[^/.]+)')
    def by_username(self, request, username=None):
        
        objects_list = list(User.objects.order_by('-score'))
        
        try:
            user = User.objects.get(username=username)
            try:
                position = objects_list.index(User.objects.get(pk=user.pk)) + 1  # Adding 1 to make it 1-indexed
            except ValueError:
                position = None  
        except Exception as e:
            return Response({"error": f"User {username} not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = user.profile if user.profile else None
        link = profile.url if profile is not None else ""
        return Response(json.dumps({"username":user.username,"id":user.id,"motivation":user.motivation,"profile":link,"title":user.title,"score":user.score,"position":position}), status=status.HTTP_200_OK)
    

class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
  
    def get_queryset(self):
        
        user = self.request.user
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['post'], url_path='add-problem')
    def add_problem(self, request, pk=None):
        
        problem_id = request.data.get('problem_id')
        if not problem_id:
            return Response({"error": "Problem ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        problem = get_object_or_404(Problems, pk=problem_id)
        if request.user.problems.filter(id=problem_id).exists():
            request.user.problems.remove(problem)
            return Response({"success": f"Problem {problem_id} removed from user."}, status=status.HTTP_200_OK)
        else:
            request.user.problems.add(problem)
            return Response({"success": f"Problem {problem_id} added to user."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='add-quiz')
    def add_quiz(self, request):
        problem_item_slug = request.data.get("problem_slug")
        if not problem_item_slug:
            return Response({"error": "Problem slug is required."}, status=status.HTTP_400_BAD_REQUEST)

        problem_quiz = get_object_or_404(ProblemQuiz, slug=problem_item_slug)
        user_quiz, created = UserQuiz.objects.get_or_create(user=request.user,problem_quiz=problem_quiz)
        
        if not created:
            return Response({"error": f"Quiz {problem_item_slug} already added to user."}, status=status.HTTP_409_CONFLICT)
        else:
            user_quiz.save()
            return Response({"success": f"Quiz {problem_item_slug} added to user."}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'], url_path='submit-answer')
    def submit_answer(self, request):
        problem_item_slug = request.data.get("problem_slug")
        question_id = request.data.get("question_id")
        selected_answer_id = request.data.get("selected_answer_id")

        if not problem_item_slug or not question_id or not selected_answer_id:
            return Response({"error": "problem_slug, question_id, and selected_answer_id parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
       
            problem_quiz = ProblemQuiz.objects.get(slug=problem_item_slug)
            selected_answer = QuizQuestionAnswer.objects.get(id=selected_answer_id, quizquestion__id=question_id)
            quiz_question = QuizQuestion.objects.get(id=question_id, problem_quiz=problem_quiz)
        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

        user_quiz, _ = UserQuiz.objects.get_or_create(user=request.user, problem_quiz=problem_quiz)
        
        
        if UserAnswer.objects.filter(user=request.user, question=quiz_question).exists():
            return Response({"success": "Answer for this question already submitted."}, status=status.HTTP_409_CONFLICT)
        
      
        UserAnswer.objects.create(user=request.user, problem_item=quiz_question.problem_quiz.problem, selected_answer=selected_answer, question=quiz_question)

        
        all_questions = quiz_question.problem_quiz.questions.all().order_by('id')
        current_index = list(all_questions).index(quiz_question)
        if current_index + 1 < len(all_questions):
            user_quiz.current_question = current_index + 1
            user_quiz.save()
            next_question = all_questions[current_index + 1]
            return Response({"success": "Your answer was saved.", "next_question_id": next_question.id}, status=status.HTTP_200_OK)
        else:
            # If there are no more questions
            user_quiz.is_complete = True
            user_quiz.save()
            return Response({"success": "Quiz completed."}, status=status.HTTP_200_OK)



    @action(detail=False, methods=['post'], url_path='questions-status')
    def get_questions(self, request):
        problem_item_slug = request.data.get("problem_slug")
        user = request.user
        
        try:
            user_quiz_status = UserQuiz.objects.get(user=user,problem_quiz__slug=problem_item_slug)
        except Exception as e:
            print(e)
            user_quiz_status = False

        if user_quiz_status:
            is_full = user_quiz_status.is_full
        else:
            is_full = False

        if not problem_item_slug:
            return Response({"error": "problem_slug parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            problem_item = ProblemItem.objects.get(slug=problem_item_slug)
       
            problem_quiz = ProblemQuiz.objects.filter(problem=problem_item)

            questions_data = []
            for quiz in problem_quiz:
                questions = QuizQuestion.objects.filter(problem_quiz=quiz)
                for question in questions:
                    submitted_answer_exists = UserAnswer.objects.filter(user=user, question=question).exists()
                    
                 
                    answers_data = []
                    answers = QuizQuestionAnswer.objects.filter(quizquestion=question)
                    for answer in answers:
                        answers_data.append({
                            "id": answer.id,
                            "content": answer.content,
                            "is_correct": answer.is_correct  
                        })
                    
                    
                    questions_data.append({
                        "id": question.id,
                        "title": question.title,
                        "is_submitted": submitted_answer_exists,
                        "is_full":is_full,
                        "answers": answers_data  
                    })

            return Response(questions_data, status=status.HTTP_200_OK)
        except ProblemItem.DoesNotExist:
            return Response({"error": "Problem item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Something went wrong. {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(detail=False, methods=['post'], url_path='problem-score')
    def get_user_score(self, request):
        problem_item_slug = request.data.get("problem_slug")

        user_quiz = UserQuiz.objects.filter(user=request.user,problem_quiz__slug=problem_item_slug).first()

        if user_quiz:

            return Response({"score":user_quiz.total_score},status=status.HTTP_200_OK)

        return Response({"error": "Problem item not found."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='motivation-edit')
    def set_motivation(self, request):

      
        
        new_motivation = request.data.get('motivation')
        print(new_motivation)
        if not new_motivation:
            return Response({"error": "new bio is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.motivation = new_motivation
        request.user.save()
       
        return Response({"success": f"Your bio was modified successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated],url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        
        if not user.check_password(current_password):
            return Response({"content": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)


        if not new_password:
            return Response({"content": "New password required."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"content": "password set successfully"}, status=status.HTTP_200_OK)


class UserImageCodeView(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], url_path='submit-problem-code')
    def submit_image_code(self, request):
        problem_item_slug = request.data.get("problem_slug")
        user_quiz = UserQuiz.objects.filter(user=request.user, problem_quiz__slug=problem_item_slug).first()

        if not user_quiz:
            return Response({"error": "Problem item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if user_quiz.image_code:
            return Response({"error": "You cannot submit an image twice."}, status=status.HTTP_200_OK)
       
        image_file = request.FILES.get('image_code', None)
        if not image_file:
            return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

   
        max_size = 5 * 1024 * 1024  
        if image_file.size > max_size:
            return Response({"error": "Image too large. Maximum size allowed is 5MB."}, status=status.HTTP_400_BAD_REQUEST)

      
        try:
            user_quiz.image_code = image_file
            user_quiz.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "your code was saved and waiting for review, you will receive a notification when it's validated"}, status=status.HTTP_200_OK)
    
    

class UserUpdate(UpdateAPIView):
    
    queryset = get_user_model().objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser,MultiPartParser]
    
    def get_object(self):
      
        return self.request.user

    def get_queryset(self):
      
        user = self.request.user
        return get_user_model().objects.filter(id=user.id)
    

    
    
class UserCreate(CreateAPIView):
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        try:
            user = get_user_model().objects.create(username=username, password=password,email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED,data={"status": "success","content":"User created"})
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"User {username} already exists "})
        
    
