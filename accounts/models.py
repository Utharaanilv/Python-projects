from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # ✅ Store default address

    def __str__(self):
        return f"{self.user.username}'s Profile"

def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.save()
        UserProfile.objects.create(
            user=user,
            phone=self.cleaned_data['phone']
        )
    return user