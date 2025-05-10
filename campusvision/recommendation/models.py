from django.db import models
from django.contrib.auth.models import User
from areas.models import Area

class RecommendationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} → {self.area.name if self.area else 'None'}"
