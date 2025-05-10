from django.urls import path
from .views import make_reservation, get_unavailable_rooms

urlpatterns = [
    path('make/', make_reservation, name='make_reservation'),
    path('unavailable/', get_unavailable_rooms, name='get_unavailable_rooms'),
]
