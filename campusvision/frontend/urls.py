from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect, name='root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('quiet-zone/', views.quiet_zone_map, name='quiet_zone'),
    path('real-time/', views.real_time_occupancy, name='real_time_occupancy'),
    path('lost-and-found/', views.lost_and_found, name='lost_and_found'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('reserve/', views.room_reservation, name='room_reservation'),
    path('make-reservation/', views.make_reservation, name='make_reservation'),  # ✅ Bu satırı ekledik
]
