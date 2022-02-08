from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from delilahdawgapi.models import RareUser
from django.http import HttpResponseServerError

class RareUserView(ViewSet):

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        
        rareuser = RareUser.objects.get(user=request.auth.user)
        
        try: 
            
            rareuser = rareuser.objects.get(pk=pk)
        except RareUser.DoesNotExist:
            return Response(
                {'message': 'Subscription does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "POST":
            try:
                
                rareuser.following.add(rareuser)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})
            
        elif request.method == "DELETE":
            try:
                
                rareuser.following.remove(rareuser)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})
    
    
    
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