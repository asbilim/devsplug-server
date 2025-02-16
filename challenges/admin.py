from django.contrib import admin
from .models import (
    Problems, 
    Attachment, 
    ProblemItem,
    Ratings, 
    ProblemSolution,
    ProblemItemSubmission,
    Comments,
    Dislikes,
    Likes,
    Challenge,
    Solution
)

# Legacy system admin
admin.site.register(Problems)
admin.site.register(ProblemItem)
admin.site.register(Attachment)
admin.site.register(ProblemSolution)
admin.site.register(ProblemItemSubmission)

# Rating and interaction admin
admin.site.register(Ratings)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Dislikes)

# New challenge system admin
admin.site.register(Challenge)
admin.site.register(Solution)