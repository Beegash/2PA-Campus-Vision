from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    user = request.user
    print('DEBUG - first_name:', user.first_name)
    print('DEBUG - last_name:', user.last_name)
    print('DEBUG - email:', user.email)
    print('DEBUG - username:', user.username)
    context = {
        "full_name_user": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "username": user.username,
    }
    return render(request, "profile.html", context) 
