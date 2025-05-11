from rest_framework import viewsets, status
from .models import IssueReport
from .serializers import IssueReportSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    renderer_classes = [JSONRenderer]
    parser_classes = [MultiPartParser, FormParser]  # 🔥 image + form verisini desteklemesi için

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return IssueReport.objects.filter(user=user)
        return IssueReport.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        # Report ID örneği üret (ID yerine modelde özel alan varsa onu koyabilirsin)
        report_id = f"MR-{serializer.instance.pk:04d}"

        return Response({"status": "success", "report_id": report_id}, status=status.HTTP_201_CREATED)
