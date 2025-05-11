from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LostItemViewSet, lost_and_found_page

router = DefaultRouter()
router.register(r'', LostItemViewSet, basename='lostitems')

urlpatterns = [
    path('api/', include(router.urls)),  # API endpointleri
    path('page/', lost_and_found_page, name='lost_and_found_page'),  # HTML sayfası
]
