from django.db import HttpResponseServerError
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from delilahdawgapi.models import Subscription


class SubscriptionView(ViewSet):
    """DelilahDawg Subscription"""
    
    def create(self,request):
        
        subscription = Subscription()
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

class SubscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields =('id', 'created_on', 'ended_on')