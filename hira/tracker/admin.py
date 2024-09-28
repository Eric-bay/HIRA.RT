from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
import openpyxl
from .models import Request, Requester, Buyer, EmailModel


# Updated export function
def export_requests_excel(modeladmin, request, queryset):
    """
    Export selected requests to Excel.
    """
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Requests'

    # Write header row
    headers = ['Reference', 'Request Type', 'Subject', 'Requester', 'Status', 'Created At', 'Updated At', 'Entered By']
    worksheet.append(headers)

    # Write data rows
    for req in queryset:
        row = [
            req.reference,
            req.request_type,
            req.subject,
            req.requester.name if req.requester else '',
            req.status,
            req.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            req.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            req.entered_by.username if req.entered_by else ''  # Convert User object to username or leave blank if None
        ]
        worksheet.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="requests.xlsx"'

    workbook.save(response)
    return response

export_requests_excel.short_description = "Export Selected Requests to Excel"

class RequestAdminForm(forms.ModelForm):
    new_comments_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        required=False
    )
    
    class Meta:
        model = Request
        fields = '__all__'
        widgets = {
            'comments_text': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

class RequestAdmin(admin.ModelAdmin):
    form = RequestAdminForm
    list_display = ('reference', 'request_type', 'subject', 'status', 'request_status', 'requester', 'buyer','entered_by', 'created_at')
    readonly_fields = ('reference', 'entered_by', 'created_at', 'updated_at', 'object_field', 'comments_text')
    fields = ('request_type', 'requester', 'buyer','status', 'request_status', 'reference', 'subject', 'created_at', 'updated_at', 'comments_text', 'object_field', 'attachments', 'new_comments_text')
    actions = [export_requests_excel]
    change_form_template = 'admin/tracker/request/change_form.html'  # Custom template
    search_fields =     search_fields = [
        'requester__name',  # Related field search
        'request_type',
        'reference',
        'created_at',
        'entered_by__username',  # Assuming you have a User model with username
        'subject',
    ]
    list_display = ['requester', 'request_type', 'reference', 'created_at', 'entered_by', 'subject']

    # Override get_urls to add custom send_mail view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_mail/<int:request_id>/', self.admin_site.admin_view(self.send_mail_view), name='request_send_mail'),
        ]
        return custom_urls + urls
    
    # Send mail view
    def send_mail_view(self, request, request_id):
        request_obj = self.get_object(request, request_id)
        if request_obj:
            # Example of sending an email
            send_mail(
                subject=f'Request Update: {request_obj.reference}',
                message=f'This is an email regarding your request {request_obj.reference}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request_obj.requester.email],
                fail_silently=False,
            )
            self.message_user(request, "Email sent successfully.")
        else:
            self.message_user(request, "Request not found.", level=messages.ERROR)
        return redirect(f'/admin/tracker/request/{request_id}/change/')

    def save_model(self, request, obj, form, change):
        if 'new_comments_text' in form.cleaned_data and form.cleaned_data['new_comments_text']:
            obj.comments_text += f"\n{form.cleaned_data['new_comments_text']}"
        if not change or obj.entered_by is None:
            obj.entered_by = request.user    
        super().save_model(request, obj, form, change)  

admin.site.register(Request, RequestAdmin)

class RequesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')    


class EmailModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'status')

admin.site.register(Requester, RequesterAdmin)
admin.site.register(EmailModel, EmailModelAdmin)
admin.site.register(Buyer)



