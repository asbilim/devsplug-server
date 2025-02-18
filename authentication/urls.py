from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import (
    UserViewSet,
    UserUpdate,
    UserCreate,
    LeaderView,
    UserActivate,
    UserResetApply,
    UserResetVerify,
    UserResetChange,
    UserClaimCode,
    FollowViewSet,
    SocialLoginView,
    VerifyEmailView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from rest_framework_social_oauth2.views import TokenView
from oauth2_provider import views as oauth2_views

router = DefaultRouter()

# router.register("me", UserViewSet, basename="user-data")
router.register("leaderboard", LeaderView, basename="users-leaderboard")
router.register(r'users', UserViewSet, basename='user')
router.register(r'follows', FollowViewSet, basename='follow')

# Create provider-specific views
class GithubLoginView(SocialLoginView):
    provider = 'github'

class GoogleLoginView(SocialLoginView):
    provider = 'google-oauth2'

class GitlabLoginView(SocialLoginView):
    provider = 'gitlab'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', include(router.urls), name='user'),
    path('api/user/create', UserCreate.as_view(), name="user-create"),
    path('api/user/activate', UserActivate.as_view(), name="user-activate"),
    path('api/user/update/<int:pk>', UserUpdate.as_view(), name="user-update"),
    path('api/user/password/apply', UserResetApply.as_view(), name="user-password-apply"),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/github/', GithubLoginView.as_view(), name='github_auth'),
    path('auth/google/', GoogleLoginView.as_view(), name='google_auth'),
    path('auth/gitlab/', GitlabLoginView.as_view(), name='gitlab_auth'),
]

"""
API Documentation

Note: The following endpoints are deprecated and will be removed in future versions:
- POST /api/user/activate
- POST /api/user/password/apply
- POST /api/user/password/verify
- POST /api/user/password/change
- POST /api/user/activate/code/claim

Please use the new JWT-based endpoints instead:
- GET /verify-email/?token=<jwt_token>
- POST /password-reset/
- POST /password-reset/confirm/

See the documentation for more details.
"""

"""
Social Authentication Endpoints:

POST /auth/github/
    Request:
        {
            "access_token": "oauth_token_from_github"
        }
    Response:
        {
            "access_token": "jwt_token",
            "refresh_token": "jwt_refresh_token",
            "user": {
                "id": 1,
                "username": "githubuser",
                "email": "user@example.com"
            }
        }

POST /auth/google/
    Request:
        {
            "access_token": "oauth_token_from_google"
        }
    Response: Same as GitHub

POST /auth/gitlab/
    Request:
        {
            "access_token": "oauth_token_from_gitlab"
        }
    Response: Same as GitHub

All endpoints return 400 for invalid tokens or authentication failures.
"""
