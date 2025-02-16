from .views import (ProblemsViewset, ProblemItemViewset,
                   RatingViewset, ProblemSolutionView, CommentView, LikeView,
                   DisLikeView, ReportView, ChallengeViewSet, SolutionViewSet,
                   CommentViewSet, LikeViewSet, DislikeViewSet)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("problems", ProblemsViewset, basename="problems-data")
router.register("problem", ProblemItemViewset, basename="problems-item-details")
router.register("ratings/problem", RatingViewset, basename="problem-quiz-rating")
router.register("solution", ProblemSolutionView, basename="problem-solution")
router.register("comments", CommentView, basename="problem-solution-comment")
router.register("likes", LikeView, basename="problem-solution-like")
router.register("dislikes", DisLikeView, basename="problem-solution-dislike")
router.register("reports", ReportView, basename="problem-solution-report")
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'solutions', SolutionViewSet, basename='solution')

# Create nested routers for solution-related endpoints
solution_router = DefaultRouter()
solution_router.register(r'comments', CommentViewSet, basename='solution-comment')
solution_router.register(r'likes', LikeViewSet, basename='solution-like')
solution_router.register(r'dislikes', DislikeViewSet, basename='solution-dislike')

urlpatterns = [
    path("", include(router.urls)),
    path('solutions/<int:solution_pk>/', include(solution_router.urls)),
]
