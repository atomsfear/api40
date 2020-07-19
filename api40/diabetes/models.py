from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(User):
    phone = models.CharField(max_length=17)

    def __str__(self):
        return self.username


class EmailAuth(models.Model):
    code = models.CharField(max_length=25)
    end_time = models.DecimalField(max_digits=10, decimal_places=0)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE)
