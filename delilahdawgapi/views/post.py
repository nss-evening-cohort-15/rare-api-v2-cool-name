from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from delilahdawgapi.models import Post, RareUser, Reaction, Category, Tag
from django.contrib.auth.models import User


class PostView(ViewSet):

    def create(self, request):

        rareuser = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["categoryId"])
        reaction = Reaction.objects.get(pk=request.data["reactionId"])
        tag = Tag.object.get(pk=request.data["tagId"])

        post = Post()
        post.title = request.data["title"]
        post.category = request.data["category"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.rareuser = rareuser
        post.reaction = reaction
        post.category = category
        post.tag = tag

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        rareuser = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["categoryId"])
        reaction = Reaction.objects.get(pk=request.data["reactionId"])
        tag = Tag.object.get(pk=request.data["tagId"])

        post = Post()
        post.title = request.data["title"]
        post.category = request.data["category"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.rareuser = rareuser
        post.reaction = reaction
        post.category = category
        post.tag = tag
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        posts = Post.objects.all()

        category = self.request.query_params.get('type', None)
        if category is not None:
            posts = posts.filter(category_id=category)

        reaction = self.request.query_params.get('type', None)
        if reaction is not None:
            posts = posts.filter(reaction_id=reaction)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class PostRareUserSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ['user', 'bio', 'profile_image_url', 'created_on', 'active']

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['label']


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['label', 'image_url']


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['label']


class PostSerializer(serializers.ModelSerializer):
    rare_user = PostRareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'rare_user', 'title', 'reaction', 'category',
                  'publication_date', 'image_url', 'content', 'approved', 'tag')

# 'rare_user',
