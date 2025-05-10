from rest_framework import viewsets
from .models import OccupancyData
from .serializers import OccupancySerializer
from rest_framework.renderers import JSONRenderer


class OccupancyViewSet(viewsets.ModelViewSet):
    queryset = OccupancyData.objects.all()
    serializer_class = OccupancySerializer
    renderer_classes = [JSONRenderer]
