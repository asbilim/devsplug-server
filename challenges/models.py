from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


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
    attachments = models.ManyToManyField(Attachment,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:

        ordering = ("points",)

    


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