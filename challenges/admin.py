from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import (
    Attachment, 
    Challenge,
    Solution,
    Comment,
    Like,
    Dislike
)

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

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['user', 'solution', 'created_at', 'content_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ['user', 'solution', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(Dislike)
class DislikeAdmin(ModelAdmin):
    list_display = ['user', 'solution', 'created_at']
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