from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'networkcoverage', views.NetworkCoverageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('coverage-by-address/', views.NetworkCoverageViewSet.as_view({'post': 'coverage_by_address'})),
]
