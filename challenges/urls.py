from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeViewSet,
    SolutionViewSet,
    CommentViewSet,
    LikeViewSet,
    DislikeViewSet,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'listings', ChallengeViewSet)
router.register(r'solutions', SolutionViewSet, basename='solution')

# Nested routes for comments and reactions
solution_router = DefaultRouter()
solution_router.register(r'comments', CommentViewSet, basename='solution-comments')
solution_router.register(r'likes', LikeViewSet, basename='solution-likes')
solution_router.register(r'dislikes', DislikeViewSet, basename='solution-dislikes')

urlpatterns = [
    path('', include(router.urls)),
    path('solutions/<int:solution_pk>/', include(solution_router.urls)),
]
