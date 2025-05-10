from django.urls import path
from .views import RealTimeOccupancyAPIView

urlpatterns = [
    path("api/real-time/", RealTimeOccupancyAPIView.as_view(), name="real_time_occupancy"),
    path("api/categories/", get_categories, name="get_categories"),  # 🔥 bu satırı ekle

]
