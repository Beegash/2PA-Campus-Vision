from django.db import models

class Area(models.Model):
    CATEGORY_CHOICES = [
        ('study', 'Study Room'),
        ('lab', 'Lab'),
        ('classroom', 'Classroom'),
    ]

    LABEL_CHOICES = [
        ('quiet', 'Sessiz'),
        ('group', 'Toplu'),
        ('mixed', 'Karma'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200)
    features = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, default='mixed')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='study')  # ✨ Yeni eklendi

    def __str__(self):
        return self.name
