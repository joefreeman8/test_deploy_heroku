from rest_framework import serializers
from ..models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Brewery
        fields = '__all__'

