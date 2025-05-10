from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from .models import Area
from .serializers import AreaSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    renderer_classes = [JSONRenderer]
