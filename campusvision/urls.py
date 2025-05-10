from django.urls import path
from . import views

urlpatterns = [
    path('api/submit-maintenance-report/', views.submit_maintenance_report, name='submit_maintenance_report'),
    path('api/get-user-reports/', views.get_user_reports, name='get_user_reports'),
    path('login/', views.login_view, name='login'),
] 
