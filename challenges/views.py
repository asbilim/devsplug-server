from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
import logging
import traceback
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from .models import Challenge, Solution, Comment, Like, Dislike, Category, UserChallenge
from .serializers import (
    ChallengeSerializer,
    ChallengeListSerializer,
    ChallengeDetailSerializer,
    SolutionSerializer,
    CommentSerializer,
    LikeSerializer,
    DislikeSerializer,
    CategorySerializer,
    UserProgressSerializer,
    UserChallengeSerializer,
    PublicSolutionSerializer
)

logger = logging.getLogger(__name__)

# New Core Endpoints

class CategoryViewSet(ReadOnlyModelViewSet):
    """Category listing and details"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ChallengePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ChallengeViewSet(ModelViewSet):
    """Main challenge endpoints"""
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    pagination_class = ChallengePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ChallengeListSerializer
        elif self.action == 'retrieve':
            return ChallengeDetailSerializer
        return ChallengeSerializer

    def get_queryset(self):
        queryset = Challenge.objects.all()
        
        # Search is handled automatically by SearchFilter
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
            
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        # Filter by tags
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()
            
        return queryset

    @extend_schema(
        description="Get the authenticated user's challenge progress, including completed challenges and statistics",
        responses={
            200: UserProgressSerializer,
            401: {"description": "Authentication is required"}
        }
    )
    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        """Get the authenticated user's challenge progress"""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserProgressSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        description="Submit a solution for a challenge. Users cannot submit multiple solutions with the same programming language for a challenge.",
        request=SolutionSerializer,
        responses={
            201: SolutionSerializer,
            400: {"description": "Bad request, including cases where the user has already submitted a solution in the specified language"},
            404: {"description": "Challenge not found"}
        }
    )
    @action(detail=True, methods=['post'])
    def submit_solution(self, request, slug=None):
        challenge = self.get_object()
        serializer = SolutionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, challenge=challenge)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Subscribe the authenticated user to a challenge",
        responses={
            201: UserChallengeSerializer,
            200: UserChallengeSerializer,
            401: {"description": "Authentication is required"},
            500: {"description": "Internal server error"}
        }
    )
    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, slug=None):
        try:
            challenge = self.get_object()
            user = request.user
            
            if not user.is_authenticated:
                return Response(
                    {"error": "Authentication required"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            subscription, created = UserChallenge.objects.get_or_create(
                user=user,
                challenge=challenge,
                defaults={'is_subscribed': True}
            )
            
            if not created and not subscription.is_subscribed:
                subscription.is_subscribed = True
                subscription.save()
            
            serializer = UserChallengeSerializer(subscription)
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
            
        except Exception as e:
            logger.error(f"Error in subscribe action: {str(e)}", exc_info=True)
            return Response(
                {"error": "Unable to process subscription"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Unsubscribe the authenticated user from a challenge",
        responses={
            204: {"description": "Successfully unsubscribed"},
            401: {"description": "Authentication is required"},
            404: {"description": "Not subscribed to this challenge"}
        }
    )
    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, slug=None):
        challenge = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            subscription = UserChallenge.objects.get(
                user=user,
                challenge=challenge
            )
            subscription.is_subscribed = False
            subscription.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserChallenge.DoesNotExist:
            return Response(
                {'detail': 'Not subscribed to this challenge.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        description="Check if the authenticated user is subscribed to this challenge",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "is_subscribed": {"type": "boolean", "description": "Whether the user is subscribed to this challenge"},
                    "authenticated": {"type": "boolean", "description": "Whether the user is authenticated"}
                }
            },
            500: {"description": "Internal server error"}
        }
    )
    @action(detail=True, methods=['get'])
    def check_subscription(self, request, slug=None):
        """Check if the authenticated user is subscribed to this challenge"""
        try:
            challenge = self.get_object()
            user = request.user
            
            # Check if user is authenticated
            if not user.is_authenticated:
                return Response({
                    'is_subscribed': False,
                    'authenticated': False,
                    'message': 'User is not authenticated'
                }, status=status.HTTP_200_OK)
            
            subscription = UserChallenge.objects.filter(
                user=user,
                challenge=challenge,
                is_subscribed=True
            ).exists()
            
            return Response({
                'is_subscribed': subscription,
                'authenticated': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error checking subscription: {str(e)}", exc_info=True)
            return Response(
                {"error": "Unable to check subscription status"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Check if the authenticated user has registered for this challenge",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "is_registered": {"type": "boolean", "description": "Whether the user has registered for this challenge"},
                    "authenticated": {"type": "boolean", "description": "Whether the user is authenticated"}
                }
            },
            401: {"description": "Authentication is required"},
            500: {"description": "Internal server error"}
        }
    )
    @action(detail=True, methods=['get'])
    def check_registration(self, request, slug=None):
        """Check if the authenticated user has registered this challenge"""
        try:
            challenge = self.get_object()
            user = request.user
            
            # Check if user is authenticated
            if not user.is_authenticated:
                return Response({
                    'is_registered': False,
                    'authenticated': False,
                    'message': 'User is not authenticated'
                }, status=status.HTTP_200_OK)
            
            # Check if user has any solutions for this challenge
            is_registered = Solution.objects.filter(
                user=user,
                challenge=challenge
            ).exists()
            
            return Response({
                'is_registered': is_registered,
                'authenticated': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error checking registration: {str(e)}", exc_info=True)
            return Response(
                {"error": "Unable to check registration status"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Get all challenges the authenticated user has subscribed to",
        responses={
            200: UserChallengeSerializer(many=True),
            401: {"description": "Authentication is required"}
        }
    )
    @action(detail=False, methods=['get'])
    def my_subscriptions(self, request):
        """Get all challenges the authenticated user has subscribed to"""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        subscribed_challenges = UserChallenge.objects.filter(
            user=request.user,
            is_subscribed=True
        ).select_related('challenge').order_by('-subscribed_at')
        
        serializer = UserChallengeSerializer(subscribed_challenges, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(
                f"Error retrieving challenge: {str(e)}\n"
                f"Path: {request.path}\n"
                f"Method: {request.method}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            return Response(
                {"error": "Unable to retrieve challenge details"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SolutionViewSet(ModelViewSet):
    """Solution management endpoints"""
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Solution.objects.filter(
                Q(user=self.request.user) | 
                Q(is_private=False)
            )
        return Solution.objects.filter(is_private=False)

    def perform_create(self, serializer):
        # Get challenge from URL parameters or request data
        challenge_id = self.request.data.get('challenge')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        serializer.save(user=self.request.user, challenge=challenge)

    @extend_schema(
        description="List all public solutions grouped by challenges"
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """List all public solutions with creator information, grouped by challenges"""
        queryset = Solution.objects.filter(is_private=False).select_related('user', 'challenge')
        
        # Apply filters
        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__iexact=language)
        
        # Apply search filter if provided
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | 
                Q(user__username__icontains=search)
            )
        
        # Order by challenge and then by creation date
        queryset = queryset.order_by('challenge__title', '-created_at')
        
        # Group solutions by challenge
        solutions_by_challenge = {}
        for solution in queryset:
            challenge_id = solution.challenge.id
            challenge_title = solution.challenge.title
            
            if challenge_id not in solutions_by_challenge:
                solutions_by_challenge[challenge_id] = {
                    'challenge': {
                        'id': challenge_id,
                        'title': challenge_title,
                        'slug': solution.challenge.slug,
                        'difficulty': solution.challenge.difficulty
                    },
                    'solutions': []
                }
            
            solutions_by_challenge[challenge_id]['solutions'].append({
                'id': solution.id,
                'user': {
                    'id': solution.user.id,
                    'username': solution.user.username,
                    'email': solution.user.email,
                    'profile': solution.user.profile.url if solution.user.profile else None
                },
                'code': solution.code,
                'documentation': solution.documentation,
                'language': solution.language,
                'status': solution.status,
                'created_at': solution.created_at,
                'likes_count': solution.likes.count(),
                'comments_count': solution.comments.count()
            })
        
        # Convert to list for response
        result = list(solutions_by_challenge.values())
        
        return Response(result)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Handling swagger schema generation
            return Comment.objects.none()
        return Comment.objects.filter(solution_id=self.kwargs['solution_pk'])

    def perform_create(self, serializer):
        solution = get_object_or_404(Solution, pk=self.kwargs['solution_pk'])
        serializer.save(user=self.request.user, solution=solution)

class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Handling swagger schema generation
            return Like.objects.none()
        return Like.objects.filter(solution_id=self.kwargs['solution_pk'])

    def perform_create(self, serializer):
        solution = get_object_or_404(Solution, pk=self.kwargs['solution_pk'])
        serializer.save(user=self.request.user, solution=solution)

class DislikeViewSet(ModelViewSet):
    serializer_class = DislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Handling swagger schema generation
            return Dislike.objects.none()
        return Dislike.objects.filter(solution_id=self.kwargs['solution_pk'])

class UserChallengeViewSet(ReadOnlyModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'challenge__slug'
    
    def get_queryset(self):
        return UserChallenge.objects.filter(
            user=self.request.user,
            is_subscribed=True
        ).select_related('challenge').order_by('-subscribed_at')

def your_view(request):
    try:
        # Your view logic here
        pass
    except Exception as e:
        logger.error(f"Error in your_view: {str(e)}", exc_info=True)
        return HttpResponse("Internal Server Error", status=500)