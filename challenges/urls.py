from .views import ProblemsViewset,ProblemItemViewset,ProblemQuizView,RatingViewset
from django.urls import path,include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("problems",ProblemsViewset,basename="problems-data")
router.register("problem",ProblemItemViewset,basename="problems-item-details")
router.register("problem-quiz",ProblemQuizView,basename="problem-quiz-details")
router.register("ratings/problem",RatingViewset,basename="problem-quiz-rating")


urlpatterns = [
    path("",include(router.urls))
]
