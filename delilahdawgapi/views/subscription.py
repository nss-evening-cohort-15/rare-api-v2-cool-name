from django.http import HttpResponseServerError
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from delilahdawgapi.models import Subscription, RareUser, rareuser, subscription


class SubscriptionView(ViewSet):
    """DelilahDawg Subscription"""
    
    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        
        rareuser = RareUser.objects.get(user=request.auth.user)
        
        try: 
            
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response(
                {'message': 'Subscription does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "POST":
            try:
                
                subscription.followers.add(rareuser)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})
            
        elif request.method == "DELETE":
            try:
                
                subscription.followers.remove(rareuser)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})
            
        
    
    
    
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
        
        rareuser = RareUser.objects.get(user=request.auth.user)
        subscriptions = Subscription.objects.get(all)
        
        for subscription in subscriptions:
            
            subscription.joined = rareuser in subscription.followers.all()
            
    
    
    
class SubscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields =('id', 'created_on', 'ended_on')