from django.urls import path
from .views import submit_report

urlpatterns = [
    path("submit-report/", submit_report, name="submit_report"),
]
