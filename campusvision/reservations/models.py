from django.db import models
from django.contrib.auth.models import User
from areas.models import Area

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} → {self.area.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
