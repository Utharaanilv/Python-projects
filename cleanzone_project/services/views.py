from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Service

def service_list(request):
    services = Service.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'services/service_list.html', {'services': services})
