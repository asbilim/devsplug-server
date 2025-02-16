from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Challenge, Solution, Comment, Like, Dislike
from .serializer import (
    ChallengeSerializer,
    SolutionSerializer,
    CommentSerializer,
    LikeSerializer,
    DislikeSerializer
)

# New Core Endpoints

class ChallengeViewSet(ModelViewSet):
    """Main challenge endpoints"""
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True, methods=['post'])
    def submit_solution(self, request, pk=None):
        challenge = self.get_object()
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, challenge=challenge)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolutionViewSet(ModelViewSet):
    """Solution management endpoints"""
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Solution.objects.filter(
                Q(user=self.request.user) | 
                Q(is_private=False)
            )
        return Solution.objects.filter(is_private=False)

    def perform_create(self, serializer):
        # Get challenge from URL parameters or request data
        challenge_id = self.request.data.get('challenge')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        serializer.save(user=self.request.user, challenge=challenge)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(solution_id=self.kwargs['solution_pk'])

    def perform_create(self, serializer):
        solution = get_object_or_404(Solution, pk=self.kwargs['solution_pk'])
        serializer.save(user=self.request.user, solution=solution)

class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(solution_id=self.kwargs['solution_pk'])

    def perform_create(self, serializer):
        solution = get_object_or_404(Solution, pk=self.kwargs['solution_pk'])
        serializer.save(user=self.request.user, solution=solution)

class DislikeViewSet(ModelViewSet):
    serializer_class = DislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dislike.objects.filter(solution_id=self.kwargs['solution_pk'])