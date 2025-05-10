from django.contrib import admin
from .models import OccupancyData
from .models import Room

admin.site.register(OccupancyData)


admin.site.register(Room)
