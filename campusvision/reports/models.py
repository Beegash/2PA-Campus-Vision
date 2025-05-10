from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class MaintenanceReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('assigned', 'Assigned'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low - Not Urgent'),
        ('medium', 'Medium - Needs Attention'),
        ('high', 'High - Urgent Issue'),
        ('emergency', 'Emergency - Immediate Action Required'),
    ]
    
    building = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.CharField(max_length=20, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            # Generate report ID in format MR-YYYY-XXXX
            year = datetime.now().year
            last_report = MaintenanceReport.objects.filter(
                report_id__startswith=f'MR-{year}-'
            ).order_by('-report_id').first()
            
            if last_report:
                last_number = int(last_report.report_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.report_id = f'MR-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.report_id} - {self.issue_type}"
