from rest_framework import viewsets
from .models import RecommendationLog
from .serializers import RecommendationLogSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic import recommend_area  # eğer ayrı dosyaya koyduysan
from django.utils.dateparse import parse_datetime
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = RecommendationLog.objects.all()
    serializer_class = RecommendationLogSerializer
    renderer_classes = [JSONRenderer]

class RecommendAreaView(APIView):
    def get(self, request):
        start_time = parse_datetime(request.query_params.get('start'))
        end_time = parse_datetime(request.query_params.get('end'))

        if not start_time or not end_time:
            return Response({"error": "start ve end parametreleri gereklidir"}, status=status.HTTP_400_BAD_REQUEST)

        recommended = recommend_area(start_time, end_time, user=request.user)

        if recommended:
            return Response({"area_id": recommended.id, "area_name": recommended.name})
        else:
            return Response({"message": "Uygun alan bulunamadı"}, status=status.HTTP_404_NOT_FOUND)
      
    