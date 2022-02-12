from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from delilahdawgapi.models import RareUser, Post
from django.http import HttpResponseServerError
from .post import PostSerializer

class RareUserView(ViewSet):

    def list(self, request):

        rareuser = RareUser.objects.get(user=request.auth.user)
        # rareuser = RareUser.objects.all()

        rareuser = RareUserSerializer(
            rareuser, many=False, context={'request': request}
        )

        profile = {}
        # profile.user = request.data["user"]
        profile["rareuser"] = rareuser.data

        return Response(profile)

    def retrieve(self,request, pk=None):
        """GEt request for single Comment"""
        
        try: 
            
            rareuser = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rareuser, context={'request': request })
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=["GET"], detail=True)
    def posts(self,request, pk=None):
        user_posts = Post.objects.filter(rare_user=pk)
        serializer = PostSerializer(user_posts, context={'request: request'}, many=True)
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_superuser', 'is_staff')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url',
        'created_on', 'active')