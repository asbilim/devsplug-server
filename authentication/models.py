import shutil
from django.db import models
from challenges.models import Problems,ProblemQuiz,ProblemItem,UserAnswer
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import os
from django.conf import settings
class User(AbstractUser):

   
    motivation = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    profile = models.ImageField(null=True, blank=True)
    problems = models.ManyToManyField(Problems)
    title = models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(null=True, blank=True,unique=True)
    def __str__(self):

        return self.username
    
    def save(self, *args, **kwargs):
        if self.score < 500:
            self.title = 'Beginner'  
        elif self.score < 1000:
            self.title = 'Novice'  
        elif self.score < 1500:
            self.title = 'Developer'  
        elif self.score < 2500:
            self.title = 'Engineer' 
        elif self.score < 4000:
            self.title = 'Architect' 
        elif self.score < 6000:
            self.title = 'Hacker'  
        elif self.score < 8500:
            self.title = 'Master'  
        elif self.score < 12000:
            self.title = 'Expert'  
        elif self.score < 16000:
            self.title = 'Guru'  
        elif self.score < 20000:
            self.title = 'Champion'  
        else:
            self.title = 'Legend'  
        print(f"Setting title to: {self.title}")
        super().save(*args, **kwargs)

    class Meta:

        ordering = ('-score','username')

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
            self.user.save()
            self.is_noted = True

        if self.image_code:
            self.is_full = True

        super().save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        # Custom logic before the actual deletion

        # Example: Reduce user score (adjust the logic based on how you want to reduce the score)
        if self.user.score and self.total_score:
            self.user.score -= self.total_score
            self.user.save()

        # Delete the folder associated with this instance
        folder_path = os.path.join(settings.MEDIA_ROOT, f'problems/codes/{self.problem_quiz.slug}/{slugify(self.user.username)}')
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

        # Call the superclass method to handle default deletion
        super().delete(*args, **kwargs)

class UserQuestionAttempt(models.Model):

    user= models.ForeignKey("authentication.User", on_delete=models.CASCADE,null=True,blank=True)
    problem = models.ForeignKey(ProblemItem,on_delete=models.CASCADE)
    answers = models.ManyToManyField(UserAnswer)
    current_question = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.user} for {self.problem.title}"