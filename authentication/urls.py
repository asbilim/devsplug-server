from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet
from rest_framework.routers import SimpleRouter
from .views import UserViewSet,UserUpdate,UserCreate,UserImageCodeView,LeaderView,UserActivate

router = SimpleRouter()

router.register("/me",UserViewSet,basename="user-data")
router.register("/code",UserImageCodeView,basename="user-image-code")
router.register("/leaderboard",LeaderView,basename="users-leaderboard")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user',include(router.urls,namespace=""), name='user'),
    path('api/user/create',UserCreate.as_view(),name="user-create"),
    path('api/user/activate',UserActivate.as_view(),name="user-activate"),
    path('api/user/update/<int:pk>',UserUpdate.as_view(),name="user-update"),
]
