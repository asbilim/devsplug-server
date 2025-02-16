from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
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
    content = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=50)
    level = models.CharField(choices=(("easy","easy"),("medium","medium"),("hard","hard")),max_length=255)
    description = models.TextField(null=True,blank=True)
    image=models.ImageField(null=True, blank=True,upload_to="challenges-image/")
    attachments = models.ManyToManyField(Attachment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:

        ordering = ("-created_at",)

    


class Problems(models.Model):

    title = models.TextField(unique=True)
    slug = models.SlugField(max_length=1500,null=True, blank=True)
    tags = TaggableManager()
    content = models.TextField(null=True, blank=True)
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

    user = models.ForeignKey("authentication.User", 
                            on_delete=models.CASCADE,
                            related_name='legacy_comments')
    problem_solution = models.ForeignKey(ProblemSolution,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='replies', null=True, blank=True)


    def __str__(self):

        return f"{self.user.username} said {self.content[:100]}..."
    
class Likes(models.Model):
    user = models.ForeignKey("authentication.User", 
                            on_delete=models.CASCADE,
                            related_name='legacy_likes')
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

    user = models.ForeignKey("authentication.User", 
                            on_delete=models.CASCADE,
                            related_name='legacy_dislikes')
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

# Core Challenge Models
class Challenge(models.Model):
    """Main challenge model replacing ProblemItem"""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        max_length=10
    )
    points = models.IntegerField(default=50)
    tags = TaggableManager()
    attachments = models.ManyToManyField('Attachment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Solution(models.Model):
    """Simplified solution model"""
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending',
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'challenge']
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new and self.status == 'accepted':
            self.user.add_points(self.challenge.points)

class Comment(models.Model):
    """Model to store comments on a solution."""
    user = models.ForeignKey('authentication.User', 
                            on_delete=models.CASCADE, 
                            related_name="challenge_comments")
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

class Like(models.Model):
    """Model for likes on a solution."""
    user = models.ForeignKey('authentication.User', 
                            on_delete=models.CASCADE, 
                            related_name="challenge_likes")
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked solution {self.solution.id}"

class Dislike(models.Model):
    """Model for dislikes on a solution."""
    user = models.ForeignKey('authentication.User', 
                            on_delete=models.CASCADE, 
                            related_name="challenge_dislikes")
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} disliked solution {self.solution.id}"
    