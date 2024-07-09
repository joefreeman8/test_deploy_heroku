from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework.exceptions import NotFound
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Brewery
from .serializers.common import BrewerySerializer
from .serializers.populated import PopulatedBrewerySerializer


class BreweryListView(APIView):
    
    def get(self, _request):
        breweries = Brewery.objects.all()
        serialized_breweries = PopulatedBrewerySerializer(breweries, many=True)
        return Response(serialized_breweries.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        brewery_to_add = BrewerySerializer(data=request.data)
        try:
            brewery_to_add.is_valid() 
            brewery_to_add.save()
            return Response(brewery_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BreweryDetailView(APIView):

    def get_brewery(self, pk):
        try:
            return Brewery.objects.get(pk=pk)
        except Brewery.DoesNotExist:
            raise NotFound(detail="Can't find that brewery")
        
    def get(self, _request, pk):
        brewery = self.get_brewery(pk=pk)
        serialized_brewery = PopulatedBrewerySerializer(brewery)
        return Response(serialized_brewery.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        brewery_to_update = self.get_brewery(pk=pk)
        updated_brewery = BrewerySerializer(brewery_to_update, data=request.data)

        if updated_brewery.is_valid():
            updated_brewery.save()
            return Response(updated_brewery.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_brewery.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, _request, pk):
        brewery_to_delete = self.get_brewery(pk=pk)
        brewery_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
