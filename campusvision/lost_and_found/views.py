from rest_framework import viewsets
from .models import LostItem
from .serializers import LostItemSerializer
from rest_framework.renderers import JSONRenderer

class LostItemViewSet(viewsets.ModelViewSet):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer
    renderer_classes = [JSONRenderer]

from django.shortcuts import render

def lost_and_found_page(request):
    return render(request, 'lost_and_found.html')
