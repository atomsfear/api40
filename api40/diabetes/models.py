from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Patient(User):
    phone = models.CharField(max_length=17, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    height = models.DecimalField(max_digits=19,
                                 decimal_places=16,
                                 blank=True,
                                 null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    fcm_id = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(max_digits=19,
                                 decimal_places=16,
                                 blank=True,
                                 null=True)
    fb_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='Normal')
    group = models.CharField(max_length=50, blank=True, null=True)
    unread_records_one = models.DecimalField(max_digits=10,
                                             decimal_places=0,
                                             default=0)
    unread_records_two = models.CharField(max_length=10, default='0')
    unread_records_three = models.DecimalField(max_digits=10,
                                               decimal_places=0,
                                               default=0)
    verified = models.CharField(max_length=1, default='0')
    privacy_policy = models.CharField(max_length=1, default='0')
    must_change_password = models.CharField(max_length=1, default='0')
    badge = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    login_times = models.DecimalField(max_digits=15,
                                      decimal_places=0,
                                      default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(max_length=6, default='0')

    def __str__(self):
        return self.username


class EmailAuth(models.Model):
    code = models.CharField(max_length=25)
    end_time = models.DecimalField(max_digits=10, decimal_places=0)


class Default(models.Model):
    id = models.DecimalField(max_digits=15, decimal_places=0, primary_key=True)
    user_id = models.DecimalField(max_digits=15,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    sugar_delta_max = models.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          blank=True,
                                          null=True)
    sugar_delta_min = models.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          blank=True,
                                          null=True)
    sugar_morning_max = models.DecimalField(max_digits=5,
                                            decimal_places=0,
                                            blank=True,
                                            null=True)
    sugar_morning_min = models.DecimalField(max_digits=5,
                                            decimal_places=0,
                                            blank=True,
                                            null=True)
    sugar_evening_max = models.DecimalField(max_digits=5,
                                            decimal_places=0,
                                            blank=True,
                                            null=True)
    sugar_evening_min = models.DecimalField(max_digits=5,
                                            decimal_places=0,
                                            blank=True,
                                            null=True)
    sugar_before_max = models.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           blank=True,
                                           null=True)
    sugar_before_min = models.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           blank=True,
                                           null=True)
    sugar_after_max = models.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          blank=True,
                                          null=True)
    sugar_after_min = models.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          blank=True,
                                          null=True)
    systolic_max = models.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       blank=True,
                                       null=True)
    systolic_min = models.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       blank=True,
                                       null=True)
    diastolic_max = models.DecimalField(max_digits=5,
                                        decimal_places=0,
                                        blank=True,
                                        null=True)
    diastolic_min = models.DecimalField(max_digits=5,
                                        decimal_places=0,
                                        blank=True,
                                        null=True)
    pulse_max = models.DecimalField(max_digits=5,
                                    decimal_places=0,
                                    blank=True,
                                    null=True)
    pulse_min = models.DecimalField(max_digits=5,
                                    decimal_places=0,
                                    blank=True,
                                    null=True)
    weight_max = models.DecimalField(max_digits=5,
                                     decimal_places=0,
                                     blank=True,
                                     null=True)
    weight_min = models.DecimalField(max_digits=5,
                                     decimal_places=0,
                                     blank=True,
                                     null=True)
    bmi_max = models.DecimalField(max_digits=5,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    bmi_min = models.DecimalField(max_digits=5,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    body_fat_max = models.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       blank=True,
                                       null=True)
    body_fat_min = models.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       blank=True,
                                       null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username


class Setting(models.Model):
    id = models.DecimalField(max_digits=15, decimal_places=0, primary_key=True)
    user_id = models.DecimalField(max_digits=15,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
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


class Medical(models.Model):
    id = models.DecimalField(max_digits=15, decimal_places=0, primary_key=True)
    user_id = models.DecimalField(max_digits=15,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    diabetes_type = models.DecimalField(max_digits=1,
                                        decimal_places=0,
                                        default=0)
    oad = models.CharField(max_length=1, default='0')
    insulin = models.CharField(max_length=1, default='0')
    anti_hypertensives = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username


class A1cs(models.Model):
    user_id = models.DecimalField(max_digits=15,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    a1c = models.DecimalField(max_digits=6,
                              decimal_places=0,
                              blank=True,
                              null=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username


class Drug(models.Model):
    user_id = models.DecimalField(max_digits=15,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)
    type = models.CharField(max_length=1, default='0')
    name = models.CharField(max_length=50, blank=True, null=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.username


class userblood(models.Model):
    systolic = models.FloatField(max_length=3, default=0, null=True)
    diastolic = models.FloatField(max_length=3, default=0, null=True)
    pulse = models.CharField(max_length=3, default=0, null=True)
    # pub_date=models.DateTimeField(u'發表時間',auto_now_add=True,editable=True)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # recorded_at = models.TimeField
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class userweight(models.Model):
    weight = models.DecimalField(max_digits=5,
                                 decimal_places=0,
                                 blank=True,
                                 null=True,
                                 default=0)
    body_fat = models.DecimalField(max_digits=5,
                                   decimal_places=0,
                                   blank=True,
                                   null=True,
                                   default=0)
    bmi = models.DecimalField(max_digits=5,
                              decimal_places=0,
                              blank=True,
                              null=True,
                              default=0)
    # pub_date=models.DateTimeField(u'發表時間',auto_now_add=True,editable=True)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # recorded_at = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class userbloodsugar(models.Model):
    sugar = models.DecimalField(max_digits=5,
                                decimal_places=0,
                                blank=True,
                                null=True,
                                default=0)
    timeperiod = models.DecimalField(max_digits=5,
                                     decimal_places=0,
                                     blank=True,
                                     null=True,
                                     default=0)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # recorded_at = models.TimeField
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class dietmod(models.Model):
    description = models.DecimalField(max_digits=5,
                                      decimal_places=0,
                                      blank=True,
                                      null=True,
                                      default=0)
    meal = models.DecimalField(max_digits=5,
                               decimal_places=0,
                               blank=True,
                               null=True,
                               default=0)
    tag = models.DecimalField(max_digits=5,
                              decimal_places=0,
                              blank=True,
                              null=True,
                              default=0)
    image = models.DecimalField(max_digits=5,
                                decimal_places=0,
                                blank=True,
                                null=True,
                                default=0)
    lat = models.DecimalField(max_digits=5,
                              decimal_places=2,
                              blank=True,
                              null=True,
                              default=0)
    lng = models.DecimalField(max_digits=5,
                              decimal_places=2,
                              blank=True,
                              null=True,
                              default=0)
    created_at = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class care(models.Model):
    message = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class notificationmod(models.Model):
    message = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(u'更新時間', auto_now=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        update_time = str(self.update_time)
        return update_time


class friendmod(models.Model):  #纪录是否為好友
    afriend = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='answers_user')
    bfriend = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='relay_to_user')


class receivemod(models.Model):
    areceive = models.ForeignKey(Patient,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='areceive_user')  #邀
    breceive = models.ForeignKey(Patient,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='breceive_user')  #被邀
    atype = models.CharField(max_length=25, null=True)

    accept_or_not = models.CharField(max_length=1, null=True)


# class cstmod(models.Model):#控糖团
#     friendcode = models.CharField(max_length=25)
