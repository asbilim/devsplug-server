from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
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

@admin.register(Problems)
class ProblemsAdmin(ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'tag_list']
    list_filter = ['created_at', 'tags']
    search_fields = ['title', 'description']
    readonly_fields = ['slug']
    date_hierarchy = 'created_at'

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'Tags'

@admin.register(ProblemItem)
class ProblemItemAdmin(ModelAdmin):
    list_display = ['title', 'level', 'points', 'created_at', 'tag_list']
    list_filter = ['level', 'created_at', 'tags']
    search_fields = ['title', 'description']
    readonly_fields = ['slug']
    date_hierarchy = 'created_at'
    list_editable = ['points']

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'Tags'

@admin.register(Challenge)
class ChallengeAdmin(ModelAdmin):
    list_display = ['title', 'difficulty', 'points', 'created_at', 'tag_list']
    list_filter = ['difficulty', 'created_at', 'tags']
    search_fields = ['title', 'description']
    readonly_fields = ['slug']
    date_hierarchy = 'created_at'
    list_editable = ['points']

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'Tags'

@admin.register(Solution)
class SolutionAdmin(ModelAdmin):
    list_display = ['user', 'challenge', 'language', 'status', 'created_at']
    list_filter = ['status', 'language', 'created_at']
    search_fields = ['user__username', 'challenge__title', 'code']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(ProblemSolution)
class ProblemSolutionAdmin(ModelAdmin):
    list_display = ['name', 'user', 'problem_item', 'language', 'created_at', 'is_valid']
    list_filter = ['language', 'is_valid', 'created_at']
    search_fields = ['name', 'user__username', 'problem_item__title']
    readonly_fields = ['unique_code', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(Comments)
class CommentsAdmin(ModelAdmin):
    list_display = ['user', 'problem_solution', 'created_at', 'content_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Ratings)
class RatingsAdmin(ModelAdmin):
    list_display = ['user', 'problem_item', 'score', 'created_at']
    list_filter = ['created_at', 'score']
    search_fields = ['user__username', 'message']
    date_hierarchy = 'created_at'

@admin.register(Likes)
class LikesAdmin(ModelAdmin):
    list_display = ['user', 'problem_solution', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(Dislikes)
class DislikesAdmin(ModelAdmin):
    list_display = ['user', 'problem_solution', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(Attachment)
class AttachmentAdmin(ModelAdmin):
    list_display = ['title', 'file_preview']
    search_fields = ['title']

    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_preview.short_description = 'File'