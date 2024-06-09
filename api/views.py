from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from api.models import NetworkCoverage
from api.serializers import NetworkCoverageSerializer
import requests

from api.utils.utils import lamber93_to_gps

def get_coordinates_from_address(address):
    response = requests.get(f'https://api-adresse.data.gouv.fr/search/?q={address}')
    data = response.json()
    coordinates = data['features'][0]['properties']["x"], data['features'][0]['properties']["y"]
    return coordinates

@api_view(['GET'])
def network_coverage_view(request):
    operators_dict = {"20810": "Orange"}
    address = request.GET.get('q')
    coordinates = get_coordinates_from_address(address)
    long, lat = lamber93_to_gps(coordinates[0], coordinates[1])
    point = Point(long, lat, srid=4326)
    
    # Find the nearest coverage for each operator
    operators = NetworkCoverage.objects.values_list('operator', flat=True).distinct()
    response_data = {}
    
    for operator in operators:
        coverage = NetworkCoverage.objects.filter(operator=operator).annotate(distance=Distance('location', point)).order_by('distance').first()
        if coverage:
            response_data[get_operator_name(operator)] = {
                '2G': coverage.twoG,
                '3G': coverage.threeG,
                '4G': coverage.fourG
            }

    if response_data:
        return Response(response_data)
    else:
        return Response({'error': 'No network coverage found'}, status=404)

def get_operator_name(id):
    operator_dict = {
        '20801': 'Orange',
        '20802': 'Orange',
        '20803': 'MobiquiThings',
        '20804': 'Netcom Group',
        '20805': 'Globalstar Europe',
        '20806': 'Globalstar Europe',
        '20807': 'Globalstar Europe',
        '20808': 'SFR',
        '20809': 'SFR',
        '20810': 'SFR',
        '20811': 'SFR',
        '20812': 'Hewlett-Packard France',
        '20813': 'SFR',
        '20814': 'RFF',
        '20815': 'Free mobile',
        '20816': 'Free mobile',
        '20817': 'Legos',
        '20818': 'Voxbone',
        '20819': 'Altitude infrastructure',
        '20820': 'Bouygues Telecom',
        '20821': 'Bouygues Telecom',
        '20822': 'Transatel Mobile',
        '20823': 'Syndicat mixte ouvert Charente numérique',
        '20824': 'MobiquiThings',
        '20825': 'Lycamobile',
        '20826': 'Bouygues Télécom Business distribution',
        '20827': 'Coriolis Télécom',
        '20828': 'Airmob',
        '20829': 'Cubic telecom France',
        '20830': 'Symacom',
        '20831': 'Mundio Mobile',
        '20832': 'Orange',
        '20834': 'Cellhire France',
        '20835': 'Free mobile',
        '20886': 'SEM@FOR77',
        '20888': 'Bouygues Telecom',
        '20889': 'Fondation b-com',
        '20890': 'Association Images & Réseaux',
        '20891': 'Orange',
        '20892': 'Association Plate-forme Telecom',
        '20893': 'Thales communications',
        '20894': 'Halys',
        '20895': 'Orange',
        '20896': 'Axione',
        '20897': 'Thales communications',
        '20898': 'Air France'
    }
    operator = operator_dict.get(id, 'Operador no encontrado')
    return operator
