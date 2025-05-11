# reservations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ReservationViewSet,
    make_reservation,
    get_unavailable_rooms,
    my_reservations,
    cancel_reservation,
    reserve_page,
)

router = DefaultRouter()
router.register(r'api', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', reserve_page, name='room_reservation'),
    path('make/', make_reservation, name='make_reservation'),
    path('my/', my_reservations, name='my_reservations'),
    path('cancel/', cancel_reservation, name='cancel_reservation'),
    path('api/reservations/unavailable/', get_unavailable_rooms, name='get_unavailable_rooms'),
    path('', include(router.urls)),
]
