from django.db import models
from django.core.exceptions import ValidationError  # Import ValidationError here
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings

class EmailModel(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=100)  # e.g., 'Created', 'Homologation validated'

    def __str__(self):
        return self.name

class Requester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
    ]

    TYPE_CHOICES = [
        ('Supplier creation', 'Supplier creation'),
        ('PO creation', 'PO creation'),
        ('NDA', 'NDA'),
        ('Other request', 'Other request'),
        ('Supplier assist', 'Supplier assist')
    ]

    REQUEST_STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Waiting Homologation Validation', 'Waiting Homologation Validation'),
        ('Homologation validated', 'Homologation validated'),
        ('Invitation to log done', 'Invitation to log done'),
        ('Waiting for Supplier completion', 'Waiting for Supplier completion'),
        ('Supplier info completed', 'Supplier info completed'),
        ('Waiting for SMD Validation', 'Waiting for SMD Validation'),
        ('SMD Validation Done', 'SMD Validation Done'),
        ('Supplier Assist Started', 'Supplier Assist Started'),
        ('Supplier Assist In Progress', 'Supplier Assist In Progress'),
        ('Supplier Assist Completed', 'Supplier Assist Completed'),
    ]
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Not Started')
    request_status = models.CharField(max_length=100, choices=REQUEST_STATUS_CHOICES)
    reference = models.CharField(max_length=20, unique=True, editable=False)  # Read-only field
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    comments_text = models.TextField(blank=True)  # Renamed field
    new_comments_text = models.TextField(blank=True, help_text="Add new comments here")
    object_field = models.CharField(max_length=255, editable=False)
    attachments = models.FileField(upload_to='attachments/', blank=True)
    subject = models.CharField(max_length=25, blank=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    

    def __str__(self):
        return f"{self.reference} - {self.request_type} - {self.status}"

    def generate_reference(self):
        # Get the last reference
        last_request = Request.objects.order_by('-id').first()
        last_number = 0
        if last_request and last_request.reference:
            # Extract the number from the last reference and increment
            last_number = int(last_request.reference[3:])
        return f"REQ{last_number + 1:04}"

    def save(self, *args, **kwargs):
        # Set reference only if it is not set
        if not self.pk:
            self.reference = self.generate_reference()
        if not self.object_field:
            self.object_field = f"{self.request_type}_{self.reference}_{self.requester.name}_{self.status}"
        super().save(*args, **kwargs)

    def clean(self):
        # Ensure comments_text does not exceed 350 characters
        if len(self.comments_text) > 350:
            raise ValidationError("Comments text cannot exceed 350 characters.")

class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure content does not exceed 350 characters
        if len(self.content) > 350:
            raise ValidationError("Comment content cannot exceed 350 characters.")

   
    


