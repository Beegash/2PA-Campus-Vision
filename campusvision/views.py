from django.http import JsonResponse
from .models import MaintenanceReport
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

@login_required
def submit_maintenance_report(request):
    if request.method == 'POST':
        try:
            building = request.POST.get('building')
            location = request.POST.get('location')
            issue_type = request.POST.get('issueType')
            priority = request.POST.get('priority')
            description = request.POST.get('description')
            
            # Create new maintenance report
            report = MaintenanceReport(
                building=building,
                location=location,
                issue_type=issue_type,
                priority=priority,
                description=description,
                user=request.user
            )
            report.save()
            
            return JsonResponse({
                'status': 'success',
                'report_id': report.report_id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@login_required
def get_user_reports(request):
    reports = MaintenanceReport.objects.filter(user=request.user).order_by('-created_at')
    reports_data = []
    
    for report in reports:
        reports_data.append({
            'report_id': report.report_id,
            'building': report.building,
            'location': report.location,
            'issue_type': report.issue_type,
            'priority': report.priority,
            'status': report.status,
            'created_at': report.created_at.strftime('%B %d, %Y'),
            'description': report.description
        })
    
    return JsonResponse({
        'status': 'success',
        'reports': reports_data
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Ana sayfaya yönlendir
        else:
            return render(request, 'login_c.html', {'error': 'Invalid username or password'})
    return render(request, 'login_c.html') 
