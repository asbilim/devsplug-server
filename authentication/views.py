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


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing the logged in user's data.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list containing only the current user.
        """
        user = self.request.user
        return User.objects.filter(id=user.id)


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