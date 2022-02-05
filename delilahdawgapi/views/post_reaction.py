from django.forms import ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from delilahdawgapi.models import Post, Reaction, PostReaction

class PostReactionView(ViewSet):

    def create(self, request):
        
        user = request.auth.user.rare_user
        # user = RareUser.objects.get(pk=request.data["rareuserId"])
        post = Post.objects.get(pk=request.data["postId"])
        reaction = Reaction.objects.get(pk=request.data["reactionId"])
        
        postreaction = PostReaction()
        postreaction.user = user
        postreaction.post = post
        postreaction.reaction = reaction
        
        try:
            postreaction.save()
            serializer = PostReactionSerializer(postreaction, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            postreaction = PostReaction.objects.get(pk=pk)
            postreaction.delete()
            
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except PostReaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        field = ('id', 'user', 'post', 'reaction')