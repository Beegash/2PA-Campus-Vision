from django.urls import path
from .views import make_reservation, get_unavailable_rooms
from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet
from . import views  # ✅ Burası eksikti

router = DefaultRouter()
router.register(r'', ReservationViewSet, basename='reservation')


urlpatterns = [
    path('make/', make_reservation, name='make_reservation'),
    path('unavailable/', get_unavailable_rooms, name='get_unavailable_rooms'),
    path('my/', views.my_reservations, name='my_reservations'),  # 🌟 yeni eklendi

]
