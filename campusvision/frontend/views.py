from django.shortcuts import render
from areas.models import Area 

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

