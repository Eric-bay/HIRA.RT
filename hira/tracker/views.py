from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Request, Requester, EmailModel
from .forms import RequesterForm, EmailModelForm
import pandas as pd
from django.db.models import Q
from .models import Buyer
from django.db.models import Count

# View for listing requests
def request_list(request):
    requests = Request.objects.all()
    return render(request, 'tracker/request_list.html', {'requests': requests})
    return render(request, 'request_list.html')

# View for listing requesters
def requester_list(request):
    requesters = Requester.objects.all()
    return render(request, 'tracker/requester_list.html', {'requesters': requesters})

# View for listing email models
def email_model_list(request):
    email_models = EmailModel.objects.all()
    return render(request, 'tracker/email_model_list.html', {'email_models': email_models})

# View to export requests to an Excel file
def export_requests(request):
    requests = Request.objects.all().values()
    df = pd.DataFrame(requests)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="requests.xlsx"'
    df.to_excel(response, index=False)
    return response

def search_requests(request):
    query = request.GET.get('q')
    if query:
        results = Request.objects.filter(
            Q(requester__name__icontains=query) |
            Q(request_type__icontains=query) |
            Q(reference__icontains=query) |
            Q(created_at__icontains=query) |
            Q(entered_by__name__icontains=query) |
            Q(subject__icontains=query)
        )
    else:
        results = Request.objects.all()
    
    return render(request, 'search_results.html', {'results': results})

def dashboard_view(request):
    return render(request, 'dashboard.html')  # Use your template here

def buyer_list(request):
    buyers = Buyer.objects.all()  # Fetch all buyers from the database
    return render(request, 'buyer_list.html', {'buyers': buyers})

def dashboard_view(request):
    # Stats based on request status
    status_stats = Request.objects.values('request_status').annotate(total=Count('request_status'))

    # Stats based on request type
    type_stats = Request.objects.values('request_type').annotate(total=Count('request_type'))

    # Stats based on requester
    requester_stats = Request.objects.values('requester__name').annotate(total=Count('requester'))

    # Stats based on who entered the request
    entered_by_stats = Request.objects.values('entered_by__username').annotate(total=Count('entered_by'))

    # Stats based on the creation date (day-by-day)
    created_at_stats = Request.objects.extra(select={'day': "date( created_at )"}).values('day').annotate(total=Count('id'))

    context = {
        'status_stats': status_stats,
        'type_stats': type_stats,
        'requester_stats': requester_stats,
        'entered_by_stats': entered_by_stats,
        'created_at_stats': created_at_stats,
    }

    return render(request, 'tracker/dashboard.html', context)
