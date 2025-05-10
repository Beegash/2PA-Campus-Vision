from django.db import models

class IssueReport(models.Model):
    ISSUE_TYPES = [
        ('electrical', 'Elektrik'),
        ('furniture', 'Mobilya'),
        ('equipment', 'Donanım'),
        ('other', 'Diğer')
    ]
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    resolved = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_issue_type_display()} - {self.location}"
