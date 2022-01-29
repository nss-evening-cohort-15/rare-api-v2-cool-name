from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from delilahdawgapi.models import Category
from delilahdawgapi.views.category import CategorySerializer

class CategoryView(ViewSet):
    
    def create(self, request):
    
        category = Category()
        category.label = request.data["label"]
        
        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('label')
    