from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from api.utils.gouvfr_api import APIGouvFR
from api.models import NetworkCoverage
from api.serializers import NetworkCoverageSerializer
from api.utils.converters import get_operator_name, lamber93_to_gps
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class NetworkCoverageViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving the network coverage information for a given address.
    """
    @swagger_auto_schema(
        operation_description="Retrieve network coverage for a given address.",
        manual_parameters=[
            openapi.Parameter(
                'q', openapi.IN_QUERY, description="Address to search for network coverage", type=openapi.TYPE_STRING
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Network coverage information",
                examples={
                    "application/json": {
                        "SFR": {
                            "location": [
                                2.4235892377054817,
                                48.95889881296555
                            ],
                            "distance_km": 1.5212682488999998,
                            "2G": True,
                            "3G": True,
                            "4G": True
                        },
                        "Orange": {
                            "location": [
                                2.4151181073123005,
                                48.97749931591031
                            ],
                            "distance_km": 1.33300976902,
                            "2G": True,
                            "3G": True,
                            "4G": True
                        }
                    }
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="No network coverage found")
        }
    )
    @action(detail=False, methods=['get'])
    def coverage(self, request):
        """
        Retrieves the network coverage information for a given address.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the network coverage information.
                If the network coverage is found, the response will contain a dictionary
                with the operator names as keys and the corresponding network coverage
                information as values.
                If no network coverage is found, the response will contain a dictionary
                with a single key-value pair: 'error' and the corresponding error message.

        Raises:
            None.
        """
        address = request.GET.get('q')

        if not address:
            return Response({'error': 'Missing address parameter'}, status=status.HTTP_400_BAD_REQUEST)
        coordinates = APIGouvFR().get_coordinates_from_address(address)
        x, y = coordinates[0], coordinates[1]

        # Convert Lambert93 coordinates to WGS84
        long, lat = lamber93_to_gps(x, y)
        point_wgs84 = Point(long, lat, srid=4326)

        # Transform point to Lambert 93 for distance calculations
        point = point_wgs84.transform(2154, clone=True)
        
        # Find the nearest coverage for each operator
        operators = NetworkCoverage.objects.values_list('operator', flat=True).distinct()
        response_data = {}

        MARGIN = 10000 # 10km
        for operator in operators:
            # Find the nearest coverage for the operator --> Taking only the results within 10km
            coverage = NetworkCoverage.objects.filter(operator=operator).annotate(distance=Distance('location', point)).filter(distance__lte=MARGIN).order_by('distance').first()
            if coverage:
                response_data[get_operator_name(operator)] = {
                    'location': (coverage.location.x, coverage.location.y),
                    'distance_km': coverage.distance.km,
                    '2G': coverage.twoG,
                    '3G': coverage.threeG,
                    '4G': coverage.fourG
                }

        if response_data:
            return Response(response_data)
        else:
            return Response({'error': 'No network coverage found'}, status=status.HTTP_404_NOT_FOUND)
