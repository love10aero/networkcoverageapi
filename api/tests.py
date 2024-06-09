from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import NetworkCoverage
from django.contrib.gis.geos import Point

class NetworkCoverageViewTest(APITestCase):

    def setUp(self):
        # Configura los datos iniciales para las pruebas
        NetworkCoverage.objects.create(
            operator=20810,  # Orange
            location=Point(2.3522, 48.8566, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20820,  # Bouygues Telecom
            location=Point(2.3522, 48.8566, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20815,  # Free mobile
            location=Point(2.3522, 48.8566, srid=4326),
            twoG=False,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20801,  # SFR
            location=Point(2.3522, 48.8566, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )

    def test_network_coverage_view(self):
        url = reverse('network_coverage_view')
        response = self.client.get(url, {'q': '8 bd du port'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "Orange": {
                "2G": True,
                "3G": True,
                "4G": True
            },
            "Bouygues Telecom": {
                "2G": True,
                "3G": True,
                "4G": True
            },
            "Free mobile": {
                "2G": False,
                "3G": True,
                "4G": True
            },
            "SFR": {
                "2G": True,
                "3G": True,
                "4G": True
            }
        }
        self.assertEqual(response.json(), expected_response)
