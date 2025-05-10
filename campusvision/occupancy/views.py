from django.http import JsonResponse
from .models import Room
from rest_framework import viewsets
from .models import OccupancyData
from .serializers import OccupancySerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import OccupancyData
from areas.models import Area
from django.http import JsonResponse
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import OccupancyData
from areas.models import Area

class RealTimeOccupancyAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        recent = now - timedelta(minutes=5)

        response = []
        for area in Area.objects.all():
            recent_data = OccupancyData.objects.filter(area=area, timestamp__gte=recent).order_by('-timestamp').first()
            person_count = recent_data.person_count if recent_data else 0
            status = "available" if person_count < area.capacity else "occupied"

            response.append({
                "id": area.id,
                "name": area.name,
                "category": area.category,
                "capacity": area.capacity,
                "is_available": area.is_available,
                "current_person_count": person_count,
                "status": status,
            })

        return Response(response)


def get_categories(request):
    categories = Room.objects.values_list('category', flat=True).distinct()
    return JsonResponse(list(categories), safe=False)


class OccupancyViewSet(viewsets.ModelViewSet):
    queryset = OccupancyData.objects.all()
    serializer_class = OccupancySerializer
    renderer_classes = [JSONRenderer]

class RealTimeOccupancyAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        recent = now - timedelta(minutes=5)

        response = []
        for area in Area.objects.all():
            recent_data = OccupancyData.objects.filter(area=area, timestamp__gte=recent).order_by('-timestamp').first()
            person_count = recent_data.person_count if recent_data else 0
            status = "available" if person_count < area.capacity else "occupied"

            response.append({
                "id": area.id,
                "name": area.name,
                "category": area.category,
                "capacity": area.capacity,
                "is_available": area.is_available,
                "current_person_count": person_count,
                "status": status,
            })

        return Response(response)
    

def get_real_time_occupancy(request):
    rooms = Room.objects.all()  # Hiçbir filtre yok!
    data = [
        {
            "name": room.name,
            "category": room.category,
            "capacity": room.capacity,
            "current_person_count": room.current_person_count,
            "status": room.status,
        }
        for room in rooms
    ]
    return JsonResponse(data, safe=False)
