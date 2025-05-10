from django.shortcuts import render, redirect
from areas.models import Area 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from reservations.models import Reservation

def room_reservation(request):
    areas = Area.objects.all()
    return render(request, 'room_reservation.html', {'areas': areas})

def dashboard(request):
    return render(request, 'dashboard.html')

def notifications(request):
    return render(request, 'notifications.html')

def quiet_zone_map(request):
    return render(request, 'quiet_zone_map.html')

def real_time_occupancy(request):
    return render(request, 'real_time_occupancy.html')

def lost_and_found(request):
    return render(request, 'lost_and_found.html')  

def report_issue(request):
    return render(request, 'report_an_issue.html')


@csrf_exempt
def make_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            area_id = data.get('area_id')
            reserved_by = data.get('reserved_by', 'anonymous')  # örnek olarak
            start_time = data.get('start_time')
            end_time = data.get('end_time')

            area = Area.objects.get(id=area_id)
            reservation = Reservation.objects.create(
                area=area,
                reserved_by=reserved_by,
                start_time=start_time,
                end_time=end_time
            )
            return JsonResponse({'success': True, 'reservation_id': reservation.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def root_redirect(request):
    return redirect('login')
