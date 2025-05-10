from rest_framework import viewsets
from .models import IssueReport
from .serializers import IssueReportSerializer
from rest_framework.renderers import JSONRenderer


class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    renderer_classes = [JSONRenderer]
