from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework.exceptions import NotFound
from rest_framework import status # status gives us a list of official/possible response codes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Beer
from .serializers.common import BeerSerializer
from .serializers.populated import PopulatedBeerSerializer

class BeerListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        beers = Beer.objects.all()
        serialized_beers = BeerSerializer(beers, many=True)
        return Response(serialized_beers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['owner'] = request.user.id
        beer_to_add = BeerSerializer(data=request.data)

        try:
            beer_to_add.is_valid() 
            beer_to_add.save()
            return Response(beer_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

class BeerDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # custom method to retrieve beer from db and error if not found
    def get_beer(self, pk):
        try:
            return Beer.objects.get(pk=pk)
        except Beer.DoesNotExist:
            raise NotFound(detail="Can't find that beer")

    def get(self, _request, pk):
            beer = self.get_beer(pk=pk)
            serialized_beer = PopulatedBeerSerializer(beer)
            return Response(serialized_beer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        beer_to_edit = self.get_beer(pk=pk)

        # * The if block in here gives nicer feedback then try/except for error handling
        # Check if the user is the owner or an admin/superuser
        if beer_to_edit.owner != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # # save original owner from the beer which we get
        original_owner = beer_to_edit.owner.id
        # re-assign request.data['owner'] to the original owner from the beer we want to edit (incase user changes owner in the body/postman).
        request.data['owner'] = original_owner

        updated_beer = BeerSerializer(beer_to_edit, data=request.data)

        if updated_beer.is_valid():
            updated_beer.save()
            return Response(updated_beer.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_beer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
            
    def delete(self, request, pk):
        beer_to_delete = self.get_beer(pk=pk)

        if beer_to_delete.owner != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        beer_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
