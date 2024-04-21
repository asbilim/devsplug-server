from django.contrib import admin
from .models import Problems,Attachment,ProblemItem,ProblemQuiz,QuizQuestion,QuizQuestionAnswer,Ratings,ProblemSolution,ProblemItemSubmission,Comments,Dislikes,Likes


models = [Problems,Attachment,ProblemItem,ProblemQuiz,QuizQuestion,QuizQuestionAnswer,Ratings,ProblemSolution,ProblemItemSubmission,Comments,Dislikes,Likes]

for model in models:
    admin.site.register(model)