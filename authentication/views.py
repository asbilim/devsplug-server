from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import permissions,status
from .serializer import UserCreateSerializer,UserUpdateSerializer
from rest_framework.response import Response
from .models import Problems
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

User = get_user_model()

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