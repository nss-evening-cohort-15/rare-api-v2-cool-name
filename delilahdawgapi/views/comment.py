from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from delilahdawgapi.models import Comment, RareUser, comment, rareuser, Post


class CommentView(ViewSet):

    def create(self, request):
        """Handle Creation of Comment"""

        rareuser = RareUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.author = rareuser

        post = Post.objects.get(pk=request.data["post"])
        comment.post = post

        try:
            comment.save()
            serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """GEt request for single Comment"""

        try:

            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT Requests for Comment"""

        rareuser = RareUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.author = rareuser

        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        comments = Comment.objects.all()

        post = self.request.query_params.get('post', None)
        if post is not None:
            comments = comments.filter(post=post)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = comment
        fields = ('id', 'content', 'created_on', 'post', 'author')
        depth = 1
