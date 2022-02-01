from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.test import tag
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from delilahdawgapi.models import Tag, RareUser, Post


class TagView(ViewSet):

    def create(self, request):

        rareuser = RareUser.objects.get(user=request.auth.user)

        tag = Tag()
        tag.label = request.data["label"]
        post = Post.objects.get(pk=request.data["post"])
        tag.post = post

        try:
            tag.save()
            serializer = TagSerializer(
                tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tag
        fields = ('id', 'title', 'post')
        depth = 1
