from .common import BrewerySerializer
from beers.serializers.common import BeerSerializer

class PopulatedBrewerySerializer(BrewerySerializer):
    beers = BeerSerializer(many=True)