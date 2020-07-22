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
