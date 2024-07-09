from .common import BeerSerializer
from breweries.serializers.common import BrewerySerializer
from comments.serializers.populated import PopulatedCommentSerializer
from jwt_auth.serializers import UserSerializer

class PopulatedBeerSerializer(BeerSerializer):
    brewery = BrewerySerializer()
    comments = PopulatedCommentSerializer(many=True)
    owner = UserSerializer()