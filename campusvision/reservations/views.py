from rest_framework import viewsets
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.renderers import JSONRenderer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    renderer_classes = [JSONRenderer]
