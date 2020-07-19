from django.http import JsonResponse
from diabetes.models import Patient, EmailAuth
from diabetes.forms import RegisterForm
from django.contrib import auth as Auth
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
import random
import string
import time
# Create your views here.


def register(request):
    result = '1'
    try:
        if request.method == 'POST':
            f = RegisterForm(request.POST)
            if f.is_valid():
                account = f.cleaned_data['account']
                phone = f.cleaned_data['phone']
                email = f.cleaned_data['email']
                password = f.cleaned_data['password']
                user = Patient.objects.create(
                    username=account, email=email, phone=phone, is_active=False)
                user.set_password(password)
                user.save()
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def auth(request):
    result = '1'
    try:
        if request.method == 'POST':
            account = request.POST.get('account', '')
            password = request.POST.get('password', '')
            if account and password:
                user = Auth.authenticate(username=account, password=password)
                if user is not None:
                    result = '0'
                else:
                    email = Patient.objects.filter(email=account)
                    if email:
                        user = Auth.authenticate(
                            username=email[0].username, password=password)
                        if user is not None:
                            result = '0'
                    else:
                        phone = Patient.objects.filter(phone=account)
                        if phone:
                            user = Auth.authenticate(
                                username=phone[0].username, password=password)
                            if user is not None:
                                result = '0'
        if result == '0':
            if user.is_active:
                request.session.create()
                Auth.login(request, user)
            else:
                result = '2'
    except:
        pass
    if result == '0':
        return JsonResponse({'status': result, 'token': request.session.session_key})
    else:
        return JsonResponse({'status': result})


def send(request):
    result = '1'
    try:
        if request.method == 'POST':
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            if phone:
                if email:
                    try:
                        user = Patient.objects.get(email=email)
                    except Patient.DoesNotExist:
                        user = None
                    if user is None:
                        user = Patient.objects.get(phone=phone)
                    if (user.email == '' or user.email != email) and (not user.is_active):
                        user.email = email
                        user.save()
                        user = Patient.objects.get(email=email)
                else:
                    user = Patient.objects.get(phone=phone)
                    if user.email == '':
                        raise Exception
                if not user.is_active:
                    duration = 3600
                    code = ''.join([random.choice(
                        string.ascii_letters + string.digits) for i in range(25)])
                    EmailAuth.objects.filter(username=user).delete()
                    EmailAuth.objects.create(code=code, end_time=int(
                        time.time()+duration), username=user)
                    title = "meter123.com 信箱驗證碼"
                    msg = 'code：' + code + '\nExpire：' + \
                        time.strftime('%Y/%m/%d %H:%M:%S %z',
                                      time.localtime(time.time()+duration))
                    email_from = 'secretclubonly007@gmail.com'
                    reciever = [user.email]
                    send_mail(title, msg, email_from,
                              reciever, fail_silently=False)
                    result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def check(request):
    result = '1'
    try:
        if request.method == 'POST':
            code = request.POST.get('code', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            if code and phone:
                try:
                    verify = EmailAuth.objects.get(code=code)
                    user = verify.username
                except Patient.DoesNotExist:
                    user = None
                if user is not None:
                    if not user.is_active:
                        if time.time() > verify.end_time:
                            verify.delete()
                            raise Exception
                        if user.phone != phone:
                            raise Exception
                        if email:
                            if user.email != email:
                                raise Exception
                        user.is_active = True
                        user.save()
                        verify.delete()
                        result = '0'
    except:
        pass
    return JsonResponse({'status': result})
