from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions,authentication

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
    path("users/",include('authentication.urls',namespace=''),name="authentication"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(r'^filer/', include('filer.urls')),
    path('documentation<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('challenges/',include('challenges.urls'), name='challenges'),
]
