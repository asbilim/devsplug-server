from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                               TaggitSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import (
    Challenge,
    Solution,
    Comment,
    Like,
    Dislike,
    Attachment,
    Category,
    UserChallenge
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'profile', 'title']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'title', 'file', 'description', 'file_type', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'order', 'stats']
    
    def get_stats(self, obj):
        return obj.get_stats()

class ChallengeListSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    category = CategorySerializer()
    completion_rate = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'slug', 'description', 'difficulty', 
            'points', 'tags', 'category', 'estimated_time',
            'completion_rate', 'user_status'
        ]
    
    def get_completion_rate(self, obj):
        return obj.get_completion_rate()
    
    def get_user_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            solution = Solution.objects.filter(
                user=request.user,
                challenge=obj
            ).first()
            if solution:
                return {
                    'status': solution.status,
                    'submitted_at': solution.created_at
                }
        return None

class ChallengeDetailSerializer(ChallengeListSerializer):
    attachments = AttachmentSerializer(many=True)
    prerequisites = ChallengeListSerializer(many=True)
    stats = serializers.SerializerMethodField()
    content = serializers.CharField()
    
    class Meta(ChallengeListSerializer.Meta):
        fields = ChallengeListSerializer.Meta.fields + [
            'content', 'attachments', 'prerequisites', 'stats'
        ]
    
    def get_stats(self, obj):
        stats = obj.get_stats()
        return {
            'total_attempts': stats['total_attempts'],
            'successful_attempts': stats['successful_attempts'],
            'total_likes': stats['total_likes'],
            'completion_rate': stats['completion_rate']
        }

    def get_user_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            solution = Solution.objects.filter(
                user=request.user,
                challenge=obj
            ).first()
            
            # Check subscription status
            is_subscribed = UserChallenge.objects.filter(
                user=request.user,
                challenge=obj,
                is_subscribed=True
            ).exists()
            
            status_data = {
                'is_subscribed': is_subscribed
            }
            
            if solution:
                status_data.update({
                    'solution_status': solution.status,
                    'submitted_at': solution.created_at
                })
            
            return status_data
        return None

class ChallengeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'content', 
                 'difficulty', 'points', 'tags', 'slug']
        read_only_fields = ['slug']

class SolutionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(queryset=Challenge.objects.all())
    
    class Meta:
        model = Solution
        fields = ['id', 'user', 'challenge', 'code', 'documentation', 'language', 
                 'status', 'created_at', 'is_private']
        read_only_fields = ['user', 'status']
    
    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        # When creating a new solution (not updating)
        if self.instance is None:
            challenge = data.get('challenge')
            language = data.get('language')
            
            # Check if user already has a solution for this challenge with this language
            existing_solution = Solution.objects.filter(
                user=request.user,
                challenge=challenge,
                language=language
            ).exists()
            
            if existing_solution:
                raise serializers.ValidationError({
                    "language": f"You have already submitted a solution for this challenge using {language}. Please choose a different language."
                })
        
        return data

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'parent']
        read_only_fields = ['user', 'solution']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    solution = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at', 'solution']
        read_only_fields = ['user', 'solution']

class DislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Dislike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'solution']

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeListSerializer(read_only=True)
    challenge_id = serializers.PrimaryKeyRelatedField(
        source='challenge',
        queryset=Challenge.objects.all(),
        write_only=True
    )
    attempts = serializers.SerializerMethodField()
    successful_attempts = serializers.SerializerMethodField()
    solution_status = serializers.SerializerMethodField()
    challenge_stats = serializers.SerializerMethodField()
    
    class Meta:
        model = UserChallenge
        fields = [
            'id', 'challenge', 'challenge_id', 'is_subscribed', 
            'subscribed_at', 'last_attempted_at', 'completed', 
            'completed_at', 'attempts', 'successful_attempts',
            'solution_status', 'challenge_stats'
        ]
        read_only_fields = [
            'subscribed_at', 'last_attempted_at', 
            'completed', 'completed_at'
        ]
    
    def get_attempts(self, obj):
        return obj.get_attempts()
    
    def get_successful_attempts(self, obj):
        return obj.get_successful_attempts()
    
    def get_solution_status(self, obj):
        solution = Solution.objects.filter(
            user=obj.user,
            challenge=obj.challenge
        ).order_by('-created_at').first()
        
        if solution:
            return {
                'status': solution.status,
                'submitted_at': solution.created_at,
                'language': solution.language
            }
        return None
    
    def get_challenge_stats(self, obj):
        challenge = obj.challenge
        total_attempts = Solution.objects.filter(challenge=challenge).count()
        successful_attempts = Solution.objects.filter(
            challenge=challenge,
            status='accepted'
        ).count()
        total_likes = Like.objects.filter(
            solution__challenge=challenge
        ).count()
        
        return {
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'total_likes': total_likes,
            'completion_rate': (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0
        }

class UserProgressSerializer(serializers.Serializer):
    total_challenges = serializers.IntegerField()
    completed_challenges = serializers.IntegerField()
    total_points = serializers.IntegerField()
    completion_by_category = serializers.DictField()
    recent_solutions = serializers.ListField()
    subscribed_challenges = UserChallengeSerializer(many=True, source='subscribed_challenges.all')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = instance
        solutions = Solution.objects.filter(user=user)
        completed = solutions.filter(status='accepted')
        
        # Get completion by category
        categories = Category.objects.all()
        completion_by_category = {}
        for category in categories:
            category_challenges = category.challenges.count()
            if category_challenges > 0:
                completed_in_category = completed.filter(
                    challenge__category=category
                ).count()
                completion_by_category[category.name] = {
                    'total': category_challenges,
                    'completed': completed_in_category,
                    'percentage': (completed_in_category / category_challenges) * 100
                }
        
        # Get recent solutions
        recent = solutions.order_by('-created_at')[:5]
        recent_solutions = [{
            'challenge': {
                'title': sol.challenge.title,
                'slug': sol.challenge.slug,
                'difficulty': sol.challenge.difficulty
            },
            'status': sol.status,
            'submitted_at': sol.created_at
        } for sol in recent]
        
        # Add subscribed challenges data
        subscribed = UserChallenge.objects.filter(
            user=user,
            is_subscribed=True
        ).select_related('challenge').order_by('-subscribed_at')
        
        data['subscribed_challenges'] = UserChallengeSerializer(
            subscribed, 
            many=True,
            context=self.context
        ).data
        
        return {
            'total_challenges': Challenge.objects.count(),
            'completed_challenges': completed.count(),
            'total_points': sum(sol.challenge.points for sol in completed),
            'completion_by_category': completion_by_category,
            'recent_solutions': recent_solutions,
            'subscribed_challenges': data['subscribed_challenges']
        }

class SolutionCreatorSerializer(serializers.ModelSerializer):
    """Serializer for solution creator information"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'profile', 'title']

class PublicSolutionSerializer(serializers.ModelSerializer):
    """Serializer for public solutions with creator information"""
    user = SolutionCreatorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Solution
        fields = [
            'id', 'user', 'code', 'documentation',
            'language', 'status', 'created_at', 'likes_count', 
            'comments_count'
        ]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()