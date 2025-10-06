from django.shortcuts import render

def dashboard(request):
    return render(request, 'core/index.html')

def fees(request):
    return render(request, 'fees/index.html')

def hostel(request):
    return render(request, 'hostel/index.html')

def academic_leave(request):
    return render(request, 'academic_leave/index.html')

def attachments_index(request):
    return render(request, 'attachments/index.html')

def notifications_index(request):
    return render(request, 'notifications/index.html')
