from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.models import NetworkCoverage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class NetworkCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkCoverage
        fields = ['operator', 'location', 'twoG', 'threeG', 'fourG']


class NetworkCoverageByAddressSerializer(serializers.Serializer):
    operator = serializers.CharField()
    twoG = serializers.FloatField()
    threeG = serializers.FloatField()
    fourG = serializers.FloatField()
