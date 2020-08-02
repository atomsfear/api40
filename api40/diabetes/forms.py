from django import forms
from django.core.validators import RegexValidator
from diabetes.models import Patient
import datetime


class RegisterForm(forms.Form):
    account = forms.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = forms.CharField(
        validators=[phone_regex], max_length=17, required=False)
    email = forms.EmailField(max_length=50, required=False)
    password = forms.CharField(max_length=50)

    def clean(self):
        account = self.cleaned_data['account']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        if email != "":
            if Patient.objects.filter(email=email).exists():
                raise forms.ValidationError("1")
            if Patient.objects.filter(username=email).exists():
                raise forms.ValidationError("2")
            if Patient.objects.filter(phone=email).exists():
                raise forms.ValidationError("3")
        if phone != "":
            if Patient.objects.filter(phone=phone).exists():
                raise forms.ValidationError("4")
            if Patient.objects.filter(username=phone).exists():
                raise forms.ValidationError("5")
            if Patient.objects.filter(email=phone).exists():
                raise forms.ValidationError("6")
        if Patient.objects.filter(username=account).exists():
            raise forms.ValidationError("7")
        if Patient.objects.filter(email=account).exists():
            raise forms.ValidationError("8")
        if Patient.objects.filter(phone=account).exists():
            raise forms.ValidationError("9")
        return self.cleaned_data


class PersonalInfoForm(forms.Form):
    token = forms.CharField(max_length=50, required=True)
    name = forms.CharField(max_length=50, required=False)
    birthday_regex = RegexValidator(regex=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    birthday = forms.CharField(
        validators=[birthday_regex], max_length=10, required=False)
    height = forms.DecimalField(
        max_digits=19, decimal_places=16, required=False)
    gender = forms.CharField(max_length=50, required=False)
    fcm_id = forms.CharField(max_length=50, required=False)
    address = forms.CharField(max_length=50, required=False)
    weight = forms.DecimalField(
        max_digits=19, decimal_places=16, required=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = forms.CharField(
        validators=[phone_regex], max_length=17, required=False)
    email = forms.EmailField(max_length=50, required=False)

    def clean(self):
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        gender = self.cleaned_data['gender']
        weight = self.cleaned_data['weight']
        height = self.cleaned_data['height']
        birthday = self.cleaned_data['birthday']
        if email != "":
            if Patient.objects.filter(email=email).exists():
                raise forms.ValidationError("1")
            if Patient.objects.filter(phone=email).exists():
                raise forms.ValidationError("2")
            if Patient.objects.filter(username=email).exists():
                raise forms.ValidationError("3")
        if phone != "":
            if Patient.objects.filter(email=phone).exists():
                raise forms.ValidationError("4")
            if Patient.objects.filter(phone=phone).exists():
                raise forms.ValidationError("5")
            if Patient.objects.filter(username=phone).exists():
                raise forms.ValidationError("6")
        if gender != "":
            if gender not in ['0', '1']:
                raise forms.ValidationError("7")
        if weight is not None:
            if weight <= 0:
                raise forms.ValidationError("8")
        if height is not None:
            if height <= 0:
                raise forms.ValidationError("9")
        if birthday != "":
            s = birthday.split('-')
            try:
                claim = datetime.date(
                    year=int(s[0]), month=int(s[1]), day=int(s[2]))
            except:
                raise forms.ValidationError("A")
            days = (datetime.date.today() - claim).days
            if days < 0:
                raise forms.ValidationError("B")
        return self.cleaned_data


class PersonalDefaultForm(forms.Form):
    sugar_delta_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_delta_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_morning_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_morning_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_evening_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_evening_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_before_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_before_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_after_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    sugar_after_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    systolic_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    systolic_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    diastolic_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    diastolic_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    pulse_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    pulse_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    weight_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    weight_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    bmi_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    bmi_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    body_fat_max = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)
    body_fat_min = forms.DecimalField(
        max_digits=5, decimal_places=0, required=False)


class SettingForm(forms.Form):
    after_recording = forms.CharField(max_length=1, required=False)
    no_recording_for_a_day = forms.CharField(max_length=1, required=False)
    over_max_or_under_min = forms.CharField(max_length=1, required=False)
    after_meal = forms.CharField(max_length=1, required=False)
    unit_of_sugar = forms.CharField(max_length=1, required=False)
    unit_of_weight = forms.CharField(max_length=1, required=False)
    unit_of_height = forms.CharField(max_length=1, required=False)

    def clean(self):
        after_recording = self.cleaned_data['after_recording']
        no_recording_for_a_day = self.cleaned_data['no_recording_for_a_day']
        over_max_or_under_min = self.cleaned_data['over_max_or_under_min']
        after_meal = self.cleaned_data['after_meal']
        unit_of_sugar = self.cleaned_data['unit_of_sugar']
        unit_of_weight = self.cleaned_data['unit_of_weight']
        unit_of_height = self.cleaned_data['unit_of_height']

        if after_recording != "":
            if after_recording not in ['0', '1']:
                raise forms.ValidationError("1")
        if no_recording_for_a_day != "":
            if no_recording_for_a_day not in ['0', '1']:
                raise forms.ValidationError("2")
        if over_max_or_under_min != "":
            if over_max_or_under_min not in ['0', '1']:
                raise forms.ValidationError("3")
        if after_meal != "":
            if after_meal not in ['0', '1']:
                raise forms.ValidationError("4")
        if unit_of_sugar != "":
            if unit_of_sugar not in ['0', '1']:
                raise forms.ValidationError("5")
        if unit_of_weight != "":
            if unit_of_weight not in ['0', '1']:
                raise forms.ValidationError("6")
        if unit_of_height != "":
            if unit_of_height not in ['0', '1']:
                raise forms.ValidationError("7")
        return self.cleaned_data


class MedicalForm(forms.Form):
    diabetes_type = forms.DecimalField(
        max_digits=1, decimal_places=0, required=False)
    oad = forms.CharField(max_length=1, required=False)
    insulin = forms.CharField(max_length=1, required=False)
    anti_hypertensives = forms.CharField(
        max_length=1, required=False)

    def clean(self):
        diabetes_type = self.cleaned_data['diabetes_type']
        oad = self.cleaned_data['oad']
        insulin = self.cleaned_data['insulin']
        anti_hypertensives = self.cleaned_data['anti_hypertensives']

        if diabetes_type != "":
            if diabetes_type not in [0, 1, 2, 3, 4]:
                raise forms.ValidationError("1")
        if oad != "":
            if oad not in ['0', '1']:
                raise forms.ValidationError("2")
        if insulin != "":
            if insulin not in ['0', '1']:
                raise forms.ValidationError("3")
        if anti_hypertensives != "":
            if anti_hypertensives not in ['0', '1']:
                raise forms.ValidationError("4")
        return self.cleaned_data


class A1csForm(forms.Form):
    a1c = forms.DecimalField(max_digits=6, decimal_places=0)
    recorded_at = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], required=False)


class DrugForm(forms.Form):
    type = forms.CharField(max_length=1, required=False)
    name = forms.CharField(max_length=50, required=False)
    recorded_at = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], required=False)

    def clean(self):
        type = self.cleaned_data['type']

        if type != "":
            if type not in ['0', '1']:
                raise forms.ValidationError("1")
        return self.cleaned_data
