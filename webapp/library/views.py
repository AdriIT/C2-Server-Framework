# Create your views here.
from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import generic
from django.views.generic.list import ListView
from .models import Device

# Create your views here
class DeviceListView(generic.ListView):
    model = Device
    template_name = "device_list.html"
    context_object_name = "device_list"
    queryset = Device.objects.filter(status=True).order_by("-id")
    
#    def get_context_data(self, *args, **kwargs):
#            qs = super(DeviceListView, self).get_queryset(*args, *kwargs)
#            qs = qs.order_by("-id")
#            return qs




def reverse_shell(request, device_username):
    if request.user.is_authenticated:
        username = request.user.username
        device = get_object_or_404(Device, username=device_username)
        return render(request, 'reverse_shell.html', {'device': device, 'sender': username})
    #if request.method=='POST':
    #    pass   
    else:
        return redirect('login.html')
    

def index(request):  
    return render(request, 'index.html', {})

def devices(request):
    return render(request, 'device_list.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("user is", user)
        if user is not None:
            login(request, user)
            return redirect('devices')
        else:
            messages.error(request, ("There was an error. Try again."))
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('index')
