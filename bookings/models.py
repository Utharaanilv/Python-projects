from django.db import models
from django.contrib.auth.models import User

SERVICE_CHOICES = [
    ('kitchen', 'Kitchen Cleaning'),
    ('bathroom', 'Bathroom Cleaning'),
    ('courtyard', 'Courtyard Cleaning'),
    ('deep', 'Deep Cleaning'),
    ('watertank', 'Water Tank Cleaning'),
    ('appliance', 'Appliance Cleaning'),
    ('office', 'Office Cleaning'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service_type} ({self.status})"