from django.contrib.auth.models import Group, User
import requests
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.gouvfr_api import APIGouvFR
from api.models import NetworkCoverage
from api.utils.utils import lamber93_to_gps

from .serializers import GroupSerializer, NetworkCoverageSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class NetworkCoverageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NetworkCoverage.objects.all().order_by('operator')
    serializer_class = NetworkCoverageSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    @action(detail=False, methods=['post'], url_path='coverage-by-address')
    def coverage_by_address(self, request):
        address = request.query_params.get('q')
        if not address:
            return Response({'error': 'Address not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make a request to the address API
        coordinates = APIGouvFR().get_coordinates(address)
        long, lat = coordinates[0], coordinates[1]
        
        # Retrieve network coverage based on the coordinates
        coverage = NetworkCoverage.objects.filter(long=long, lat=lat)
        serializer = self.get_serializer(coverage, many=True)
        
        return Response(serializer.data)
    

