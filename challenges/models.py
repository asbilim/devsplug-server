from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import F
from django.core.mail import send_mail
from string import ascii_letters
import random

generate_string = lambda taille: "".join([ascii_letters[random.randint(0,len(ascii_letters)-1)] for i in range(taille)])

class Attachment(models.Model):

    title = models.TextField(unique=True)
    file = models.FileField(upload_to="attachments/")


    def __str__(self):

        return self.title



class ProblemItem(models.Model):

    title = models.TextField(unique=True)
    slug = models.SlugField(max_length=1500,null=True, blank=True)
    tags = TaggableManager()
    content = RichTextUploadingField(null=True, blank=True)
    points = models.IntegerField(default=50)
    level = models.CharField(choices=(("easy","easy"),("medium","medium"),("hard","hard")),max_length=255)
    description = models.TextField(null=True,blank=True)
    image=models.ImageField(null=True, blank=True,upload_to="challenges-image/")
    attachments = models.ManyToManyField(Attachment,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:

        ordering = ("-created_at",)

    


class ProblemQuiz(models.Model):

    title = models.TextField(unique=True,null=True)
    slug = models.SlugField(max_length=1500,null=True, blank=True)
    problem = models.ForeignKey(ProblemItem, related_name="quiz",on_delete=models.CASCADE)

    def __str__(self):

        return self.title
    
    def save(self, *args, **kwargs):
        self.title = self.problem.title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class QuizQuestion(models.Model):

    title = models.TextField(unique=True)
    slug = models.SlugField(max_length=1500,null=True, blank=True)
    value = models.IntegerField()
    problem_quiz = models.ForeignKey(ProblemQuiz,related_name="questions",on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class QuizQuestionAnswer(models.Model):

    content = RichTextUploadingField()
    is_correct = models.BooleanField(default=False)
    quizquestion = models.ForeignKey(QuizQuestion,related_name="answers",on_delete=models.CASCADE)

    def __str__(self):
        
        return f"{self.is_correct} {self.quizquestion.title} {self.content}"





class Problems(models.Model):

    title = models.TextField(unique=True)
    slug = models.SlugField(max_length=1500,null=True, blank=True)
    tags = TaggableManager()
    content = RichTextUploadingField(null=True, blank=True)
    problems = models.ManyToManyField(ProblemItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Ratings(models.Model):

    score = models.DecimalField(null=True, blank=True,decimal_places=2,max_digits=10)
    message = models.TextField()
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE,related_name='ratings')
    problem_item = models.ForeignKey(ProblemItem, on_delete=models.CASCADE,related_name='ratings')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.problem_item:
            return f"{self.user} for {self.problem_item.title}"
        else:
            return f"Reply by {self.user}"

    def is_reply(self):
        """Check if the rating is a reply to another rating."""
        return self.parent is not None
    
    class Meta:

        ordering = ("-created_at",)




class UserAnswer(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="user_answers")
    problem_item = models.ForeignKey("challenges.ProblemItem", on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey("challenges.QuizQuestion", on_delete=models.CASCADE, related_name="user_answers")
    selected_answer = models.ForeignKey("challenges.QuizQuestionAnswer", on_delete=models.CASCADE, related_name="selected_by_users")
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0,blank=True, null=True)
    def save(self, *args, **kwargs):
        # Automatically check if the selected answer is correct when saving.
        self.is_correct = self.selected_answer.is_correct
        self.score = self.question.value if self.is_correct else 0
        super().save(*args, **kwargs)

    def __str__(self):
        correct_status = "Correct" if self.is_correct else "Incorrect"
        return f"{self.user.username} - {self.problem_item.title} - {self.question.title} ({correct_status})"


class ProblemItemSubmission(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="problem_submissions")
    problem_item = models.ForeignKey("challenges.ProblemItem", on_delete=models.CASCADE, related_name="submissions")
    image = models.ImageField(upload_to='problem_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)
    is_noted = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission for {self.problem_item.title} by {self.user.username}"
    
    def save(self,*args,**kwargs):

        if self.is_valid and not self.is_noted:
            self.is_noted = True
            self.user.score+=20

        super().save(*args, **kwargs)


class ProblemSolutionItem(models.Model):

    code = models.TextField()
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):

        return self.name
    
class ProblemSolution(models.Model):

    user = models.ForeignKey("authentication.User",on_delete=models.CASCADE,null=True,blank=True)
    code = models.TextField()
    name = models.CharField(max_length=250)
    unique_code = models.CharField(null=True,blank=True,max_length=255)
    parts = models.ManyToManyField(ProblemSolutionItem)
    style = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    scale = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=True)
    problem_item = models.ForeignKey(ProblemItem,on_delete=models.CASCADE,blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    

    def __str__(self):

        return f'solution for {self.problem_item.title} by {self.user.username}.'
    
    def save(self,*args,**kwargs):

        if self._state.adding:
            while True:
                code = generate_string(16)
                if not ProblemSolution.objects.filter(unique_code=code).exists():
                    self.unique_code = code
                    break
            # send_mail("Devsplug challenge submission",f"hello admin , new submission for {self.problem_item.title} by","noreply@devsplug.com",["admin@devsplug.com"])

        super().save(*args,**kwargs)

    
    class Meta:

        ordering = ("-pk",)
        unique_together = ('user','problem_item','language')  
        
class Comments(models.Model):

    user = models.ForeignKey("authentication.User",on_delete=models.CASCADE)
    problem_solution = models.ForeignKey(ProblemSolution,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='replies', null=True, blank=True)


    def __str__(self):

        return f"{self.user.username} said {self.content[:100]}..."
    
class Likes(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    problem_solution = models.ForeignKey(ProblemSolution, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.problem_solution}"

    def toggle_like(self):
        """Toggle a like for a problem solution and adjust user score accordingly."""
        if self.pk: 
            self.problem_solution.user.score = F('score') - 10  
            self.problem_solution.user.save(update_fields=['score'])
            self.delete()  
        else:
            self.save()  
            self.problem_solution.user.score +=10 
            self.problem_solution.user.save(update_fields=['score'])

    def save(self, *args, **kwargs):
        """Override save method to handle score update when like is initially added."""
        if not self.pk:  
            super().save(*args, **kwargs)  
            self.problem_solution.user.score +=  self.problem_solution.problem_item.points
            self.problem_solution.user.save(update_fields=['score'])
        else:
            super().save(*args, **kwargs)
    
class Dislikes(models.Model):

    user = models.ForeignKey("authentication.User",on_delete=models.CASCADE)
    problem_solution = models.ForeignKey(ProblemSolution,on_delete=models.CASCADE,related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} disliked {self.problem_solution}"
    

class ReportSolution(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    problem_solution = models.ForeignKey(ProblemSolution, on_delete=models.CASCADE, related_name="reports")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem_solution')  

    def save(self, *args, **kwargs):
        """Override the save method to send an email notification upon report creation."""
        is_new = self._state.adding
        super().save(*args, **kwargs) 
        if is_new:  
            send_mail(
                subject='New Problem Solution Report',
                message=f'User {self.user.username} has reported a solution with ID {self.problem_solution.id}.',
                from_email="noreply@devsplug.com",
                recipient_list=["admin@devsplug.com"],
                fail_silently=False,
            )

    