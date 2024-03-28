from django.contrib import admin
from .models import Problems,Attachment,ProblemItem,ProblemQuiz,QuizQuestion,QuizQuestionAnswer,Ratings


models = [Problems,Attachment,ProblemItem,ProblemQuiz,QuizQuestion,QuizQuestionAnswer,Ratings]

for model in models:
    admin.site.register(model)