from .views import ProblemsViewset,ProblemItemViewset,ProblemQuizView,RatingViewset,ProblemSolutionView,CommentView,LikeView,DisLikeView,ReportView
from django.urls import path,include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("problems",ProblemsViewset,basename="problems-data")
router.register("problem",ProblemItemViewset,basename="problems-item-details")
router.register("problem-quiz",ProblemQuizView,basename="problem-quiz-details")
router.register("ratings/problem",RatingViewset,basename="problem-quiz-rating")
router.register("solution",ProblemSolutionView,basename="problem-solution")
router.register("comments",CommentView,basename="problem-solution-comment")
router.register("likes",LikeView,basename="problem-solution-like")
router.register("dislikes",DisLikeView,basename="problem-solution-dislike")


urlpatterns = [
    path("",include(router.urls))
]
