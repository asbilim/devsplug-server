from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import User, Follow

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = ['username', 'email', 'score', 'title', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'title', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login', 'title']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile')}),
        ('Points & Title', {'fields': ('score', 'title', 'motivation')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ['-date_joined']

@admin.register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    date_hierarchy = 'created_at'