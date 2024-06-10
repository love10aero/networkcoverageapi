from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from rest_framework import status

from api.models import NetworkCoverage


class NetworkCoverageViewTest(TestCase):

    def setUp(self):
        # Configure initial data for tests
        NetworkCoverage.objects.create(
            operator=20810,  # Orange
            location=Point(2.066447960018601, 49.041136063459355, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20820,  # Bouygues Telecom
            location=Point(2.066447960018601, 49.041136063459355, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20815,  # Free mobile
            location=Point(2.066447960018601, 49.041136063459355, srid=4326),
            twoG=False,
            threeG=True,
            fourG=True
        )
        NetworkCoverage.objects.create(
            operator=20801,  # SFR
            location=Point(2.066447960018601, 49.041136063459355, srid=4326),
            twoG=True,
            threeG=True,
            fourG=True
        )

    def test_network_coverage_view(self):
        """
        Test the network coverage view endpoint.

        This function tests the network coverage view endpoint by sending a GET request with a query parameter 'q' set to '8 bd du port'.
        It then asserts that the response status code is 200 (OK). The expected response is a dictionary containing network coverage 
        information for different operators. The function compares each field of the expected response with the actual response,
        allowing for a tolerance of 6 decimal places for floating point numbers.
        """
        self.maxDiff = None  # Allow full diff output
        url = reverse('networkcoverage-coverage')
        response = self.client.get(url, {'q': '8 bd du port'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = {
            "SFR": {
                "location": [
                    2.066447960018601,
                    49.041136063459355
                ],
                "distance_km": 1.09058186391,
                "2G": True,
                "3G": True,
                "4G": True
            },
            "Bouygues Telecom": {
                "location": [
                    2.066447960018601,
                    49.041136063459355
                ],
                "distance_km": 1.09058186391,
                "2G": True,
                "3G": True,
                "4G": True
            },
            "Free mobile": {
                "location": [
                    2.066447960018601,
                    49.041136063459355
                ],
                "distance_km": 1.09058186391,
                "2G": False,
                "3G": True,
                "4G": True
            },
            "Orange": {
                "location": [
                    2.066447960018601,
                    49.041136063459355
                ],
                "distance_km": 1.09058186391,
                "2G": True,
                "3G": True,
                "4G": True
            }
        }

        actual_response = response.json()

        # Compare each field with tolerance for floating point numbers
        for operator, expected_data in expected_response.items():
            actual_data = actual_response.get(operator)
            self.assertIsNotNone(actual_data)
            self.assertAlmostEqual(expected_data["location"][0], actual_data["location"][0], places=6)
            self.assertAlmostEqual(expected_data["location"][1], actual_data["location"][1], places=6)
            self.assertAlmostEqual(expected_data["distance_km"], actual_data["distance_km"], places=6)
            self.assertEqual(expected_data["2G"], actual_data["2G"])
            self.assertEqual(expected_data["3G"], actual_data["3G"])
            self.assertEqual(expected_data["4G"], actual_data["4G"])

    def test_network_coverage_view_invalid_address(self):
        """
        Test the network coverage view endpoint with an invalid address.

        This function tests the network coverage view endpoint by sending a GET request
        without the required 'address' parameter. It asserts that the response status code
        is 400 (Bad Request). It also checks that the response JSON contains an 'error'
        field with the value 'Missing address parameter'.
        """
        url = reverse('networkcoverage-coverage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.content)
        actual_answer = response.json()
        self.assertEqual(actual_answer['error'], 'Missing address parameter')
