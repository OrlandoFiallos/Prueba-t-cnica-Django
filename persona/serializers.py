from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person 
        fields = ['id','document_type', 'document','names','last_names','hobbies','created_at','updated_at']