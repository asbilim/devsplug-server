from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'score', 'title', 'bio', 
                 'profile', 'followers_count', 'following_count']
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()

# Add these serializers for deprecated endpoints
class DeprecatedActivateSerializer(serializers.Serializer):
    code = serializers.CharField()

class DeprecatedResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class DeprecatedResetVerifySerializer(serializers.Serializer):
    code = serializers.CharField()

class DeprecatedResetChangeSerializer(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField()

class DeprecatedClaimCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

class UserActivateSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'}
    ) 