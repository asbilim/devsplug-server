from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

schema_view = get_schema_view(
   openapi.Info(
      title="Devsplug",
      default_version='v1',
      description="Devsplug API documentation",
      terms_of_service="",
      contact=openapi.Contact(email="info@devsplug.com"),
      license=openapi.License(name=""),
   ),
   public=False,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("users/", include('authentication.urls', namespace=''), name="authentication"),
    path('filer/', include('filer.urls')),
    path('documentation<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('challenges/', include('challenges.urls'), name='challenges'),
]

# Serve static files in production
urlpatterns += [
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Only add this if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)