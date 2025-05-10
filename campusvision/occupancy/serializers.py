from rest_framework import serializers
from .models import OccupancyData

class OccupancySerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupancyData
        fields = '__all__'
