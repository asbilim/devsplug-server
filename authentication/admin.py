from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserAnswer,UserQuestionAttempt,UserQuiz


admin.site.register(User, UserAdmin)
admin.site.register(UserQuestionAttempt)
admin.site.register(UserAnswer)
admin.site.register(UserQuiz)