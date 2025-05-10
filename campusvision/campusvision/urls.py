from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Viewset'leri içe aktar
from areas.views import AreaViewSet
from reservations.views import ReservationViewSet
from occupancy.views import OccupancyViewSet
from feedback.views import FeedbackViewSet
from lost_and_found.views import LostItemViewSet
from issues.views import IssueReportViewSet
from recommendation.views import RecommendationViewSet, RecommendAreaView  # 👈 burası önemli

# Router ayarı
router = routers.DefaultRouter()
router.register(r'areas', AreaViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'occupancy', OccupancyViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'lost', LostItemViewSet)
router.register(r'issues', IssueReportViewSet)
router.register(r'recommendation', RecommendationViewSet)

# URLPattern'lere özel endpoint'i ekle
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/recommend-area/', RecommendAreaView.as_view(), name='recommend-area'),  # 👈 burası eklendi
    path('', include('frontend.urls')),
    path("reserve/", include("reservations.urls")),
    path('occupancy/', include('occupancy.urls')),
    path('', include('users.urls')),
    path('', include('reports.urls')),
]
