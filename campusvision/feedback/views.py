from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.renderers import JSONRenderer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    renderer_classes = [JSONRenderer]
