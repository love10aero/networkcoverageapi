import requests
from rest_framework.response import Response
from rest_framework import status

class APIGouvFR:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(APIGouvFR, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_coordinates_from_address(self, address):
        # Make a request to the address API
        response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={address}")

        
        if response.status_code != 200:
            return Response({'error': 'Failed to get coordinates from address API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = response.json()
        
        if not data['features']:
            return Response({'error': 'Address could not be geocoded'}, status=status.HTTP_400_BAD_REQUEST)
        

        data = response.json()

        if not data['features']:
            return None
        
        # Get coordinates
        coordinates = data['features'][0]['properties']["x"], data['features'][0]['properties']["y"]
        return coordinates
