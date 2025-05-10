from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, RecommendAreaView

router = DefaultRouter()
router.register(r'logs', RecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommend/', RecommendAreaView.as_view(), name='recommend-area'),
]
