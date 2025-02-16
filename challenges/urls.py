from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeViewSet,
    SolutionViewSet,
    CommentViewSet,
    LikeViewSet,
    DislikeViewSet
)

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'solutions', SolutionViewSet, basename='solution')

# Nested routers for solution-related endpoints
solution_router = DefaultRouter()
solution_router.register(r'comments', CommentViewSet, basename='solution-comment')
solution_router.register(r'likes', LikeViewSet, basename='solution-like')
solution_router.register(r'dislikes', DislikeViewSet, basename='solution-dislike')

urlpatterns = [
    path('', include(router.urls)),
    path('solutions/<int:solution_pk>/', include(solution_router.urls)),
]
