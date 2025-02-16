from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VerificationCode, ResetCode, Follow

# Register User with custom UserAdmin
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(VerificationCode)
admin.site.register(ResetCode)
admin.site.register(Follow)