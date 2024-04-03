from django.db import models
from challenges.models import Problems,ProblemQuiz,ProblemItem,UserAnswer
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
class User(AbstractUser):

   
    motivation = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    profile = models.ImageField(null=True, blank=True)
    problems = models.ManyToManyField(Problems)
    title = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):

        return self.username
    
    def save(self, *args, **kwargs):

        if self.score < 1001:
            self.title =  'novice'
        elif self.score < 3001:
            self.title =  'pro'
        elif self.score < 7001:
            self.title =  'plug'
        elif self.score < 15001:
            self.title =  'champion'
        else:
            self.title =  'legend'

        super().save(*args,**kwargs)

class UserQuiz(models.Model):

    def user_directory_path(instance, filename):
       
        base_username = slugify(instance.user.username)
        return f'problems/codes/{instance.problem_quiz.slug}/{base_username}/{filename}'
    
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    problem_quiz = models.ForeignKey(ProblemQuiz,on_delete=models.CASCADE,null=True,blank=True)
    is_complete = models.BooleanField(default=False)
    current_question = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0,null=True,blank=True)
    is_noted = models.BooleanField(default=False,null=True,blank=True)
    image_code = models.ImageField(upload_to=user_directory_path, blank=True,null=True)
    is_full = models.BooleanField(default=False,null=True,blank=True)
 

    def __str__(self):

        return f"{self.user} for {self.problem_quiz.title}"
    
    def save(self,*args,**kwargs):
        
        answers_score = UserAnswer.objects.filter(user=self.user,problem_item__slug=self.problem_quiz.slug).filter(is_correct=True)
        self.total_score = sum([answer.score for answer in answers_score if answer.is_correct])
        if self.is_complete and not self.is_noted:
            self.user.score += self.total_score
            self.is_noted = True

        if self.image_code:
            self.is_full = True

        super().save(*args,**kwargs)

class UserQuestionAttempt(models.Model):

    user= models.ForeignKey("authentication.User", on_delete=models.CASCADE,null=True,blank=True)
    problem = models.ForeignKey(ProblemItem,on_delete=models.CASCADE)
    answers = models.ManyToManyField(UserAnswer)
    current_question = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.user} for {self.problem.title}"