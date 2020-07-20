from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(User):
    phone = models.CharField(max_length=17)
    name = models.CharField(max_length=50, blank=True)
    birthday = models.CharField(max_length=10, blank=True)
    height = models.DecimalField(
        max_digits=19, decimal_places=16, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True)
    fcm_id = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(
        max_digits=19, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.username


class EmailAuth(models.Model):
    code = models.CharField(max_length=25)
    end_time = models.DecimalField(max_digits=10, decimal_places=0)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE)
