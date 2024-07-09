from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework.exceptions import NotFound
from rest_framework import status # status gives us a list of official/possible response codes
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers.common import CommentSerializer
from .serializers.populated import PopulatedCommentSerializer


class CommentListView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, _request):
        comments = Comment.objects.all()
        serialized_comments = CommentSerializer(comments, many=True)
        return Response(serialized_comments.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['owner'] = request.user.id
        
        comment_to_add = CommentSerializer(data=request.data)
        try:
            comment_to_add.is_valid() 
            comment_to_add.save()
            return Response(comment_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Can't find that Comment")
        
    def get(self, _request, pk):
        comment = self.get_comment(pk=pk)
        serialized_comment = PopulatedCommentSerializer(comment)
        return Response(serialized_comment.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        comment_to_update = self.get_comment(pk=pk)

        if comment_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # # save original owner from the beer which we get
        original_owner = comment_to_update.owner.id
        # re-assign request.data['owner'] to the original owner from the beer we want to edit (incase user changes owner in the body/postman).
        request.data['owner'] = original_owner

        updated_comment = CommentSerializer(comment_to_update, data=request.data)

        if updated_comment.is_valid():
            updated_comment.save()
            return Response(updated_comment.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, request, pk):
        comment_to_delete = self.get_comment(pk=pk)

        if comment_to_delete.owner != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
