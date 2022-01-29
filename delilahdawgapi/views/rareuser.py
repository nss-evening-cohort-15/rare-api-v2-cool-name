from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from delilahdawgapi.models import RareUser

class RareUserView(ViewSet):

    def list(self, request):

        rareuser = RareUser.objects.get(user=request.auth.user)

        rareuser = RareUserSerializer(
            rareuser, many=False, context={'request': request}
        )

        rareuser = {}
        rareuser.user = request.data["user"]
        rareuser.bio = request.data["bio"]
        rareuser.profile_image_url = request.data["profile_image_url"]
        rareuser.created_on = request.data["created_on"]
        rareuser.active = request.data["active"]
        rareuser["rareuser"] = rareuser.data

        return Response(rareuser)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('user', 'bio', 'profile_image_url',
        'created_on', 'active')