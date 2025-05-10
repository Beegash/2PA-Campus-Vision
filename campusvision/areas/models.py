from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # ✨ EKLE
    location = models.CharField(max_length=200)
    features = models.TextField(blank=True, null=True)     # ✨ EKLE
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    label = models.CharField(
        max_length=20,
        choices=[('quiet', 'Sessiz'), ('group', 'Toplu'), ('mixed', 'Karma')],
        default='mixed'
    )

    def __str__(self):
        return self.name
