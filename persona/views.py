from django.shortcuts import render
from rest_framework import viewsets, status 
from .models import Person
from rest_framework.response import Response  
import datetime 
from .serializers import PersonSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .utils.filters import PersonFilter
from rest_framework.filters import SearchFilter, OrderingFilter

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(deleted_at__isnull=True)
    serializer_class = PersonSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['names','last_names','document_type']
    ordering_fields = ['created_at']
    filterset_class = PersonFilter
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = datetime.datetime.now()
        count_documents = (
            Person.objects.filter(
                document__icontains=instance.document + '_deleted'
            ).values('document').count() 
        )
        print("Count documents ", count_documents)
        instance.document = instance.document + '_deleted' + str(count_documents + 1)
        instance.save()
        return Response({'message': 'Eliminado correctamente'}, status=status.HTTP_200_OK)