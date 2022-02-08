from django.http import HttpResponseServerError
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from delilahdawgapi.models import Subscription, RareUser, rareuser, subscription
from django.contrib.auth.models import User

class SubscriptionView(ViewSet):
    """DelilahDawg Subscription"""
    
    
    
    def create(self,request):
        
        author = RareUser.objects.get(user=request.auth.user)
        follower = RareUser.objects.get(user=request.auth.user)
        
        subscription = Subscription()
        subscription.follower = follower
        subscription.author = author
        subscription.created_on = request.data["created_on"]
        subscription.ended_on = request.data["ended_on"]
        
        try:
            subscription.save()
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, pk=None):
        
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):
        
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()
            
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Subscription.DoesNotExist as ex:
            return Response ({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        rareuser = request.auth.user.rareuser
        subscriptions = Subscription.objects.all()
        
        rareuser.following.all()
            
            
        serializer = SubscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class SubscriptionUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']    
    
class SubscriptionRareuserSerializer(serializers.ModelSerializer):
    user = SubscriptionUserSerializer(many=False)
    
    class Meta:
        model = RareUser
        fields = ['user', 'bio', 'profile_image_url', 'created_on', 'active']   

class SubscriptionSerializer(serializers.ModelSerializer):
    author = SubscriptionRareuserSerializer(many=False)
    follower = SubscriptionRareuserSerializer(many=False)
    
    class Meta:
        model = Subscription
        fields =('id', 'author', 'follower', 'created_on', 'ended_on', 'joined')
        

        

