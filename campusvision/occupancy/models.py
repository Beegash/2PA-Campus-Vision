from datetime import timedelta
from django.utils import timezone
from reservations.models import Reservation
from areas.models import Area
from django.db.models import Avg
from django.db import models


class OccupancyData(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    person_count = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.area.name} - {self.person_count} kişi - {self.timestamp}"

def recommend_area(start_time, end_time, user=None, reason_log=True):
    # 1. Zaman çakışan rezervasyonları al
    overlapping_reservations = Reservation.objects.filter(
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    reserved_area_ids = overlapping_reservations.values_list('area_id', flat=True)

    # 2. Son 30 dakikadaki doluluk ortalamalarını al
    thirty_mins_ago = timezone.now() - timedelta(minutes=30)
    recent_occupancy = OccupancyData.objects.filter(timestamp__gte=thirty_mins_ago)
    avg_person_counts = recent_occupancy.values('area').annotate(avg_count=Avg('person_count'))

    # 3. Rezerve edilmemiş alanları filtrele
    available_avg = [entry for entry in avg_person_counts if entry['area'] not in reserved_area_ids]

    if not available_avg:
        if user and reason_log:
            RecommendationLog.objects.create(user=user, area=None, reason="Uygun alan bulunamadı")
        return None

    # 4. En az dolu olan alanı bul
    recommended = min(available_avg, key=lambda x: x['avg_count'])
    area = Area.objects.get(id=recommended['area'])

    if user and reason_log:
        reason = f"Ortalama kişi sayısı: {recommended['avg_count']} - En uygun alan"
        RecommendationLog.objects.create(user=user, area=area, reason=reason)

    return area