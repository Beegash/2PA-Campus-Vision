from rest_framework import viewsets
from .models import IssueReport
from .serializers import IssueReportSerializer
from rest_framework.renderers import JSONRenderer


class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        # Sadece giriş yapan kullanıcının kendi kayıtlarını döndür
        user = self.request.user
        if user.is_authenticated:
            return IssueReport.objects.filter(user=user)
        return IssueReport.objects.none()

    def perform_create(self, serializer):
        # Yeni kayıt eklerken user alanını otomatik olarak ata
        serializer.save(user=self.request.user)
