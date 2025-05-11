from django.contrib import admin
from .models import IssueReport

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'building', 'location', 'issue_type', 'priority', 'status', 'resolved', 'reported_at')
    search_fields = ('description', 'location', 'building', 'user__username')
    list_filter = ('building', 'issue_type', 'priority', 'status', 'resolved', 'reported_at')
