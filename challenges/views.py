from .serializer import ProblemItemSerializer,ProblemSerializer
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Problems,ProblemItem
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
class ProblemsViewset(ReadOnlyModelViewSet):

    serializer_class = ProblemSerializer
    queryset = Problems.objects.all()

class ProblemItemViewset(ReadOnlyModelViewSet):

    serializer_class = ProblemItemSerializer
    queryset = ProblemItem.objects.all()
    
    @action(detail=False, methods=['post'], url_path='details')
    def get_by_slug(self, request, slug=None):
        slug = request.data.get('slug')
        queryset = self.get_queryset()
        problem_item = get_object_or_404(queryset, slug=slug)
        serializer = self.get_serializer(problem_item)
        return Response(serializer.data)