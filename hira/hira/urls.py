from django.contrib import admin
from django.urls import path
from tracker import views
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('requests/', views.request_list, name='request_list'),
    path('requesters/', views.requester_list, name='requester_list'),
    path('email_models/', views.email_model_list, name='email_model_list'),
    path('export/', views.export_requests, name='export_requests'),
]

def request_list(request):
    # Fetch data if needed and pass to the template
    return render(request, 'request_list.html')

def requester_list(request):
    # Fetch data if needed and pass to the template
    return render(request, 'requester_list.html')

def email_model_list(request):
    # Fetch data if needed and pass to the template
    return render(request, 'email_model_list.html')

def export_requests(request):
    # Handle export logic
    return render(request, 'export_requests.html')

