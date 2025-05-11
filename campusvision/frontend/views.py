from django.shortcuts import render, redirect
from areas.models import Area 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from reservations.models import Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.http import require_POST

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

@login_required
def profile(request):
    user = request.user
    password_message = None

    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if not user.check_password(current_password):
            password_message = "Current password is incorrect."
        elif new_password != confirm_password:
            password_message = "New passwords do not match."
        else:
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                password_message = "Password changed successfully. Please log in again."
                logout(request)
            except Exception as e:
                password_message = str(e)

    context = {
        "full_name_user": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "username": user.username,
        "password_message": password_message,
    }
    return render(request, 'profile.html', context)

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

@require_POST
@login_required
def change_password(request):
    user = request.user
    current_password = request.POST.get('currentPassword')
    new_password = request.POST.get('newPassword')
    confirm_password = request.POST.get('confirmPassword')

    if not user.check_password(current_password):
        return JsonResponse({'success': False, 'error': 'Mevcut şifre yanlış.'})

    if new_password != confirm_password:
        return JsonResponse({'success': False, 'error': 'Yeni şifreler eşleşmiyor.'})

    try:
        validate_password(new_password, user)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)

    return JsonResponse({'success': True, 'message': 'Şifre başarıyla değiştirildi.'})
