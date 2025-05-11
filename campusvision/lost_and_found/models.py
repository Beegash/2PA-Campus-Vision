from django.db import models

class LostItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/', null=True, blank=True)
    location = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    found = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    category = models.CharField(max_length=100, default="other")

    def __str__(self):
        return self.title
