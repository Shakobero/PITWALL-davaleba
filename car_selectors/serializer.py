from rest_framework import serializers
from .models import Make, Model, CarType

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = '__all__'
