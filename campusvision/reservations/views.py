from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Reservation
from areas.models import Area
from datetime import datetime, timedelta
from .serializers import ReservationSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_GET, require_POST
from django.utils.timezone import make_aware


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    renderer_classes = [JSONRenderer]

def reserve_page(request):
    return render(request, 'room_reservation.html')

def make_reservation(request):
    if request.method == "POST":
        area_id = request.POST.get("area_id")
        date = request.POST.get("date")              # "2025-05-18"
        start_time = request.POST.get("start_time")  # "10:00 AM"
        duration = request.POST.get("duration")      # "1 hour", "2 hours", etc.

        try:
            start_dt = make_aware(datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %I:%M %p"))

            if duration == "1 hour":
                end_dt = start_dt + timedelta(hours=1)
            elif duration == "2 hours":
                end_dt = start_dt + timedelta(hours=2)
            else:
                end_dt = start_dt + timedelta(hours=3)

            area = Area.objects.get(id=area_id)

            # ÇAKIŞMA KONTROLÜ
            overlap = Reservation.objects.filter(
                area=area,
                start_time__lt=end_dt,
                end_time__gt=start_dt,
                is_cancelled=False
            ).exists()

            if overlap:
                messages.error(request, "This room is already reserved in the selected time slot.")
                return redirect("room_reservation")

            Reservation.objects.create(
                user=request.user,
                area=area,
                start_time=start_dt,
                end_time=end_dt
            )

            messages.success(request, "Room successfully reserved! 🎉")
            return redirect("room_reservation")

        except Exception as e:
            messages.error(request, f"Reservation failed: {str(e)}")

    return redirect("room_reservation")

@require_GET
def get_unavailable_rooms(request):
    from django.utils.timezone import make_aware

    date = request.GET.get("date")
    start_time = request.GET.get("start_time")
    duration = int(request.GET.get("duration", 1))

    try:
        full_start = make_aware(datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M"))
        full_end = full_start + timedelta(hours=duration)

        reservations = Reservation.objects.filter(
            start_time__lt=full_end,
            end_time__gt=full_start,
            is_cancelled=False
        )

        busy_area_ids = reservations.values_list("area_id", flat=True)
        return JsonResponse({"unavailable": list(busy_area_ids)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def my_reservations(request):
    now = timezone.now()
    upcoming = Reservation.objects.filter(user=request.user, start_time__gte=now).order_by('start_time')
    past = Reservation.objects.filter(user=request.user, start_time__lt=now).order_by('-start_time')
    return render(request, 'my_reservations.html', {
        'upcoming_reservations': upcoming,
        'past_reservations': past,
    })

@csrf_exempt
@require_POST
def cancel_reservation(request):
    reservation_id = request.POST.get("reservation_id")
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        reservation.delete()  # Veritabanından tamamen siler
        return JsonResponse({"success": True})
    except Reservation.DoesNotExist:
        return JsonResponse({"error": "Reservation not found or not yours"}, status=404)
