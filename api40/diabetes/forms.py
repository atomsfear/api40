from django import forms
from django.core.validators import RegexValidator
from diabetes.models import Patient


class RegisterForm(forms.Form):
    account = forms.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    email = forms.EmailField(max_length=50, required=False)
    password = forms.CharField(max_length=50)

    def clean(self):
        account = self.cleaned_data['account']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        if email != "":
            if Patient.objects.filter(email=email).exists():
                raise forms.ValidationError("Email exists")
            if Patient.objects.filter(email=account).exists():
                raise forms.ValidationError("1")
            if Patient.objects.filter(email=phone).exists():
                raise forms.ValidationError("2")
        if Patient.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phone exists")
        if Patient.objects.filter(username=email).exists():
            raise forms.ValidationError("3")
        if Patient.objects.filter(username=phone).exists():
            raise forms.ValidationError("4")
        if Patient.objects.filter(phone=account).exists():
            raise forms.ValidationError("5")
        if Patient.objects.filter(phone=email).exists():
            raise forms.ValidationError("6")
        return self.cleaned_data
