from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import permissions,status
from .serializer import UserCreateSerializer,UserUpdateSerializer, LeaderSerializer
from rest_framework.response import Response
from .models import VerificationCode, ResetCode, Follow
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
from .models import User
import json
from django.core.mail import send_mail
from .serializer import FollowSerializer

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
            user.is_active = False
            verification = VerificationCode.objects.create(user=user)
            otp_code = verification.generate_code()
            try:
                send_mail("Devsplug verification code",f"Hello {username} this is your Devsplug verification code : {otp_code}","noreply@devsplug.com",[email],fail_silently=False)
              
            except Exception as e:
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"could not send email to user","exists":False})

            user.save()
            return Response(status=status.HTTP_201_CREATED,data={"status": "success","content":"User created, verify your email to activate your account"})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"User {username} already exists ","exists":True})
        

class UserClaimCode(CreateAPIView):
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        username = request.data.get('username')
      
        try:
            user = get_user_model().objects.get(username=username)
            if user.is_active:
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"User {username} already activated, if you forgot your password reset it ","exists":True,"already":True})
            verification,created = VerificationCode.objects.get_or_create(user=user)
            otp_code = verification.generate_code()
            verification.save()
            try:
                send_mail("Devsplug verification code",f"Hello {username} this is your Devsplug verification code : {otp_code}","noreply@devsplug.com",[email],fail_silently=False)       
            except Exception as e:
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"could not send email to user","exists":False})

            user.save()
            return Response(status=status.HTTP_201_CREATED,data={"status": "success","content":"code sent to your email , use it to activate your account"})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"User {username} does not exists ","exists":False})
          
class UserActivate(CreateAPIView):
    
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        otp_code = request.data.get("otp")
        
        try:
            verification = VerificationCode.objects.get(code=otp_code)
            if verification:
                verification.user.is_active = True
                verification.user.save()
                verification.delete()
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "success","content":f"account activated successfully","exists":False})
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})
        


class UserResetApply(CreateAPIView):
    
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"user with the email {email} does not exist","exists":False})
        
        try:
            reset,created = ResetCode.objects.get_or_create(user=user)
            print(created)
            if reset:
                code = reset.generate_code()
                send_mail("Devsplug password verification code",f"Hello {user.username} this is your Devsplug verification code : {code}","noreply@devsplug.com",[email],fail_silently=False)
                reset.save()
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "success","content":f"an email has been send , verify to continue","exists":False})
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})
        

class UserResetVerify(CreateAPIView):
    
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        otp = request.data.get("otp")

        try:
            reset = ResetCode.objects.get(code=otp)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"user with the otp does not exist","exists":False})
        
        if reset.code == otp:
            reset.can_reset = True
            reset.save()
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "success","content":f"success, you can now change your password","exists":False})
        
        return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})


class UserResetChange(CreateAPIView):
    
    
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        
        password = request.data.get("password")
        otp = request.data.get("otp")
        try:
            reset = ResetCode.objects.get(code=otp)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"user with the email {email} does not exist","exists":False})
        
        if reset.can_reset:
            reset.user.set_password(password)
            reset.user.save()
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "success","content":f"success, password changed successfully","exists":False})
        
        return Response(status=status.HTTP_401_UNAUTHORIZED,data={"status": "error","content":f"the code is incorrect ","exists":False})

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        follower = request.user
        following_id = request.data.get("following_id")
        if not following_id:
            return Response({"error": "following_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            following = User.objects.get(id=following_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if already following; if yes then unfollow
        follow_qs = Follow.objects.filter(follower=follower, following=following)
        if follow_qs.exists():
            follow_qs.delete()
            return Response({"success": "Unfollowed successfully."}, status=status.HTTP_200_OK)
        else:
            Follow.objects.create(follower=follower, following=following)
            return Response({"success": "Followed successfully."}, status=status.HTTP_201_CREATED)