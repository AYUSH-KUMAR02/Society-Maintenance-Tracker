from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Complaint, Notice
from .forms import ComplaintForm

@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(resident=request.user).order_by('-created_at')
    notices = Notice.objects.order_by('-is_important', '-created_at')
    return render(request, 'dashboard.html', {'complaints': complaints, 'notices': notices})

@login_required
def raise_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.resident = request.user
        complaint.save()
        return redirect('dashboard')
    return render(request, 'raise_complaint.html', {'form': form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, resident=request.user)
    return render(request, 'complaint_detail.html', {'complaint': complaint})

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/register.html', {'form': form})