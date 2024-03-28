from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet
from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter()

router.register("/me",UserViewSet,basename="user-data")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user',include(router.urls,namespace=""), name='user'),
]
