from django.db import models
from challenges.models import Problems
from django.contrib.auth.models import AbstractUser

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

