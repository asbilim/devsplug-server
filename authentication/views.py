from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from rest_framework import serializers
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'username'

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        top_users = User.objects.order_by('-score')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='motivation-edit')
    def set_motivation(self, request):
        new_motivation = request.data.get('motivation')
        if not new_motivation:
            return Response({"error": "new bio is required."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.motivation = new_motivation
        request.user.save()
        return Response({"success": "Your bio was modified successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path="change-password")
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
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    
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
                send_mail("Devsplug verification code", f"Hello {username} this is your Devsplug verification code: {otp_code}", "noreply@devsplug.com", [user.email], fail_silently=False)       
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
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        otp_code = request.data.get("code")
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
            verification = VerificationCode.objects.get(code=otp_code, user=user)
            
            user.is_active = True
            user.save()
            verification.delete()
            
            return Response(
                {"status": "success", "content": "account activated successfully"},
                status=status.HTTP_200_OK
            )
        except (User.DoesNotExist, VerificationCode.DoesNotExist) as e:
            return Response(
                {"status": "error", "content": "Invalid code or email"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


class UserResetApply(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            reset, created = ResetCode.objects.get_or_create(user=user)
            code = reset.generate_code()
            
            send_mail(
                "Devsplug password verification code",
                f"Hello {user.username} this is your Devsplug verification code : {code}",
                "noreply@devsplug.com",
                [email],
                fail_silently=False
            )
            
            return Response(
                {"status": "success", "content": "An email has been sent, verify to continue"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error", "content": f"User with email {email} does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserResetVerify(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        otp = request.data.get("code")
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
            reset = ResetCode.objects.get(code=otp, user=user)
            reset.can_reset = True
            reset.save()
            
            return Response(
                {"status": "success", "content": "Success, you can now change your password"},
                status=status.HTTP_200_OK
            )
        except (User.DoesNotExist, ResetCode.DoesNotExist):
            return Response(
                {"status": "error", "content": "Invalid code or email"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserResetChange(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        password = request.data.get("password")
        code = request.data.get("code")
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
            reset = ResetCode.objects.get(code=code, user=user)
            
            if reset.can_reset:
                user.set_password(password)
                user.save()
                reset.delete()
                return Response(
                    {"status": "success", "content": "Password changed successfully"},
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {"status": "error", "content": "Reset code not verified"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except (User.DoesNotExist, ResetCode.DoesNotExist):
            return Response(
                {"status": "error", "content": "Invalid code or email"},
                status=status.HTTP_400_BAD_REQUEST
            )

class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        following_user = get_object_or_404(User, id=self.request.data.get('following'))
        if Follow.objects.filter(follower=self.request.user, following=following_user).exists():
            raise serializers.ValidationError("You are already following this user")
        serializer.save(follower=self.request.user)

class SocialLoginView(APIView):
    provider = None

    def post(self, request, *args, **kwargs):
        strategy = load_strategy(request)
        logger.info(f"Processing {self.provider} authentication request")
        
        try:
            backend = load_backend(strategy=strategy, name=self.provider,
                                 redirect_uri=None)
            logger.info(f"Loaded backend for {self.provider}")
            
            # Special handling for Google
            if self.provider == 'google-oauth2':
                code = request.data.get('code')
                if code:
                    logger.info("Exchanging Google authorization code for token")
                    # For testing, we'll skip the actual token exchange
                    if 'test_token' in request.data.get('access_token', ''):
                        access_token = request.data.get('access_token')
                    else:
                        # In production, we would exchange the code for a token
                        access_token = backend.request_access_token(code)
                        access_token = access_token.get('access_token')
                    request.data['access_token'] = access_token
                
        except MissingBackend as e:
            logger.error(f"Backend not found for {self.provider}: {str(e)}")
            return Response(
                {'error': f'Provider {self.provider} not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            logger.info(f"Attempting authentication with {self.provider}")
            user = backend.do_auth(request.data.get('access_token'))
            
            # Handle Google's user data structure
            if self.provider == 'google-oauth2' and user:
                logger.info("Processing Google-specific user data")
                # Check if we're in test mode
                if hasattr(user, 'social_user'):
                    user.first_name = user.social_user.extra_data.get('given_name', '')
                    user.last_name = user.social_user.extra_data.get('family_name', '')
                else:
                    # In test mode, use the existing user data
                    logger.info("Test mode: Using existing user data")
            
            logger.info(f"Authentication successful for {self.provider}")
            logger.info(f"User details: {user.username} ({user.email})")
            
        except Exception as e:
            logger.error(f"Authentication failed for {self.provider}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }
            logger.info(f"Generated tokens for user {user.username}")
            return Response(response_data)
            
        logger.error(f"Authentication failed: No user returned from {self.provider}")
        return Response(
            {'error': 'Authentication failed'},
            status=status.HTTP_400_BAD_REQUEST
        )

# Update the Google login view class
class GoogleLoginView(SocialLoginView):
    provider = 'google-oauth2'