from django.db import models
from django.contrib.auth.models import User

class IssueReport(models.Model):
    ISSUE_TYPES = [
        ('electrical', 'Elektrik'),
        ('furniture', 'Mobilya'),
        ('equipment', 'Donanım'),
        ('plumbing', 'Tesisat'),
        ('hvac', 'HVAC/Isıtma-Soğutma'),
        ('structural', 'Yapısal'),
        ('cleaning', 'Temizlik'),
        ('technology', 'Teknoloji'),
        ('other', 'Diğer')
    ]
    PRIORITY_LEVELS = [
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
        ('emergency', 'Acil')
    ]
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('in_progress', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
        ('assigned', 'Atandı')
    ]
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    resolved = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_reports')
    building = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_issue_type_display()} - {self.location}"
