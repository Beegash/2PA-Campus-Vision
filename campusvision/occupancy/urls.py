from django.urls import path
from .views import RealTimeOccupancyAPIView
from .views import get_categories
from .views import get_real_time_occupancy


urlpatterns = [
    path("api/real-time/", RealTimeOccupancyAPIView.as_view(), name="real_time_occupancy"),
    path("api/categories/", get_categories, name="get_categories"),  # 🔥 bu satırı ekle
    path("real-time-json/", get_real_time_occupancy, name="real_time_occupancy"),

]
