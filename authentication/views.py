from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializer import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing the logged in user's data.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list containing only the current user.
        """
        user = self.request.user
        return User.objects.filter(id=user.id)
