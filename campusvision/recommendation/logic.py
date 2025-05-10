from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg
from reservations.models import Reservation
from occupancy.models import OccupancyData
from areas.models import Area
from .models import RecommendationLog

def recommend_area(start_time, end_time, user=None, reason_log=True):
    overlapping = Reservation.objects.filter(start_time__lt=end_time, end_time__gt=start_time)
    reserved_ids = overlapping.values_list('area_id', flat=True)

    recent = OccupancyData.objects.filter(timestamp__gte=timezone.now() - timedelta(minutes=30))
    avg_counts = recent.values('area').annotate(avg_count=Avg('person_count'))

    available = [entry for entry in avg_counts if entry['area'] not in reserved_ids]
    if not available:
        if user and reason_log:
            RecommendationLog.objects.create(user=user, area=None, reason="Uygun alan bulunamadı")
        return None

    best = min(available, key=lambda x: x['avg_count'])
    area = Area.objects.get(id=best['area'])

    if user and reason_log:
        reason = f"Ortalama kişi sayısı: {best['avg_count']} - En uygun alan"
        RecommendationLog.objects.create(user=user, area=area, reason=reason)

    return area
