from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

from .models import Reservation
from .serializers import ReservationSerializer
from areas.models import Area

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    renderer_classes = [JSONRenderer]


def reserve_page(request):
    return render(request, 'room_reservation.html')


@login_required
@require_POST
def make_reservation(request):
    area_id = request.POST.get("area_id")
    date = request.POST.get("date")  # "2025-05-18"
    try:
        # Sabit saat aralığı
        start_dt = make_aware(datetime.strptime(f"{date} 10:00 AM", "%Y-%m-%d %I:%M %p"))
        end_dt = start_dt + timedelta(hours=1)

        area = Area.objects.get(id=area_id)

        overlap = Reservation.objects.filter(
            area=area,
            start_time__lt=end_dt,
            end_time__gt=start_dt,
            is_cancelled=False
        ).exists()

        if overlap:
            messages.error(request, "This room is already reserved on this date.")
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
    """
    Beklenen query parametre:
    - date: "2025-05-18"
    """
    try:
        date_str = request.GET.get("date")
        if not date_str:
            return JsonResponse({"error": "Missing date parameter"}, status=400)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_dt = make_aware(datetime.combine(date, datetime.min.time()))
        end_dt = make_aware(datetime.combine(date, datetime.max.time()))

        reservations = Reservation.objects.filter(
            start_time__lt=end_dt,
            end_time__gt=start_dt,
            is_cancelled=False
        )

        busy_area_ids = reservations.values_list("area__room_id", flat=True)
        return JsonResponse({"rooms": list(busy_area_ids)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

from django.contrib.auth.decorators import login_required

@login_required
def my_reservations(request):
    now = timezone.now()

    upcoming = Reservation.objects.filter(user=request.user, start_time__gte=now, is_cancelled=False).order_by('start_time')
    past = Reservation.objects.filter(user=request.user, start_time__lt=now, is_cancelled=False).order_by('-start_time')

    return render(request, 'my_reservations.html', {
        'upcoming_reservations': upcoming,
        'past_reservations': past,
    })

from django.contrib.auth.decorators import login_required

@login_required
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
        reservation.delete()
        return JsonResponse({"success": True})
    except Reservation.DoesNotExist:
        return JsonResponse({"error": "Reservation not found or not yours"}, status=404)
