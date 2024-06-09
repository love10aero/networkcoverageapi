from django.urls import path
from api.views import network_coverage_view

urlpatterns = [
    path('coverage/', network_coverage_view, name='network_coverage_view'),
]
