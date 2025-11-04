from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking

RATING_CHOICES = [
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
]

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.rating} Stars"
    
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)