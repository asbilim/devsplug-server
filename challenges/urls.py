from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    ChallengeViewSet,
    SolutionViewSet,
    CommentViewSet,
    LikeViewSet,
    DislikeViewSet,
    CategoryViewSet,
    UserChallengeViewSet
)

router = DefaultRouter()
router.register(r'listings', ChallengeViewSet, basename='challenge')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'solutions', SolutionViewSet, basename='solution')

# Create a nested router for subscriptions
challenge_router = routers.NestedDefaultRouter(router, r'listings', lookup='challenge')
challenge_router.register(r'subscribe', UserChallengeViewSet, basename='challenge-subscription')

solutions_router = routers.NestedDefaultRouter(router, r'listings', lookup='challenge')
solutions_router.register(r'solutions', SolutionViewSet, basename='challenge-solution')

comments_router = routers.NestedDefaultRouter(solutions_router, r'solutions', lookup='solution')
comments_router.register(r'comments', CommentViewSet, basename='solution-comment')

likes_router = routers.NestedDefaultRouter(solutions_router, r'solutions', lookup='solution')
likes_router.register(r'likes', LikeViewSet, basename='solution-like')

dislikes_router = routers.NestedDefaultRouter(solutions_router, r'solutions', lookup='solution')
dislikes_router.register(r'dislikes', DislikeViewSet, basename='solution-dislike')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(challenge_router.urls)),
    path('', include(solutions_router.urls)),
    path('', include(comments_router.urls)),
    path('', include(likes_router.urls)),
    path('', include(dislikes_router.urls)),
    path('listings/<slug:slug>/subscribe/', ChallengeViewSet.as_view({'post': 'subscribe'}), name='challenge-subscribe'),
    path('listings/<slug:slug>/unsubscribe/', ChallengeViewSet.as_view({'post': 'unsubscribe'}), name='challenge-unsubscribe'),
    path('listings/<slug:slug>/check-subscription/', ChallengeViewSet.as_view({'get': 'check_subscription'}), name='challenge-check-subscription'),
]
