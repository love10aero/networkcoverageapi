from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from api.views import NetworkCoverageViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Network Coverage API",
      default_version='v1',
      description="API for retrieving network coverage information",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@networkcoverage.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Create a router for version 1 of the API
router_v1 = DefaultRouter()
router_v1.register(r'networkcoverage', NetworkCoverageViewSet, basename='networkcoverage')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include(router_v1.urls)),
]
