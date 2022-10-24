from djongo import models
from django.contrib.auth.models import User


# Create your models here.
class UserProperties(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    isPremium = models.BooleanField()