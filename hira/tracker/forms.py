from django import forms
from .models import Request, Requester, EmailModel, Buyer

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['buyer', 'requester', 'subject', 'comments_text', 'new_comments_text']  # Include all required fields
        exclude = ['reference', 'created_at', 'updated_at', 'object_field', 'attachments']
        widgets = {
            'comments_text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'new_comments_text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class RequesterForm(forms.ModelForm):
    class Meta:
        model = Requester
        fields = ['user', 'email', 'name']

class EmailModelForm(forms.ModelForm):
    class Meta:
        model = EmailModel
        fields = ['name', 'subject', 'body', 'status']


