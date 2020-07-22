from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
# Create your models here.


class Patient(User):
    phone = models.CharField(max_length=17, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    height = models.DecimalField(
        max_digits=19, decimal_places=16, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    fcm_id = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=19, decimal_places=16, blank=True, null=True)
    fb_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='Normal')
    group = models.CharField(max_length=50, blank=True, null=True)
    unread_records_one = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    unread_records_two = models.CharField(max_length=10, default='0')
    unread_records_three = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    verified = models.CharField(max_length=1, default='0')
    privacy_policy = models.CharField(max_length=1, default='0')
    must_change_password = models.CharField(max_length=1, default='0')
    badge = models.DecimalField(
        max_digits=15, decimal_places=0, default=0)
    login_times = models.DecimalField(
        max_digits=15, decimal_places=0, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class EmailAuth(models.Model):
    code = models.CharField(max_length=25)
    end_time = models.DecimalField(max_digits=10, decimal_places=0)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Default(models.Model):
    id = models.DecimalField(
        max_digits=15, decimal_places=0, primary_key=True)
    user_id = models.DecimalField(
        max_digits=15, decimal_places=0, blank=True, null=True)
    sugar_delta_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_delta_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_morning_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_morning_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_evening_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_evening_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_before_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_before_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_after_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_after_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    systolic_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    systolic_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    diastolic_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    diastolic_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    pulse_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    pulse_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    weight_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    weight_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    bmi_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    bmi_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    body_fat_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    body_fat_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username


class Setting(models.Model):
    id = models.DecimalField(
        max_digits=15, decimal_places=0, primary_key=True)
    user_id = models.DecimalField(
        max_digits=15, decimal_places=0, blank=True, null=True)
    after_recording = models.CharField(max_length=1, default='0')
    no_recording_for_a_day = models.CharField(max_length=1, default='0')
    over_max_or_under_min = models.CharField(max_length=1, default='0')
    after_meal = models.CharField(max_length=1, default='0')
    unit_of_sugar = models.CharField(max_length=1, default='0')
    unit_of_weight = models.CharField(max_length=1, default='0')
    unit_of_height = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username
