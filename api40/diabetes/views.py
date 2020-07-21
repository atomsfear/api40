from django.http import JsonResponse
from diabetes.models import Patient, EmailAuth
from diabetes.forms import RegisterForm, PersonalInfoForm
from django.contrib import auth as Auth
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone
from django.http.multipartparser import MultiPartParser
import random
import string
import time
# Create your views here.


def register(request):
    # 1.註冊
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
    # 2.登入
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
    # 3.發送驗證碼
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


def vcheck(request):
    # 4.檢查驗證碼
    result = '1'
    try:
        if request.method == 'POST':
            code = request.POST.get('code', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            if code and phone:
                verify = EmailAuth.objects.get(code=code)
                user = verify.username
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


def forgot(request):
    # 5.忘記密碼
    result = '1'
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
            else:
                user = Patient.objects.get(phone=phone)
            if not user.is_active:
                raise Exception
            new_password = ''.join([random.choice(
                string.ascii_letters + string.digits) for i in range(12)])
            title = "meter123.com 新密碼"
            msg = '請使用新密碼登入！！\n新密碼：' + new_password
            email_from = 'secretclubonly007@gmail.com'
            reciever = [user.email]
            send_mail(title, msg, email_from,
                      reciever, fail_silently=False)
            user.set_password(new_password)
            user.save()
            unexpired_sessions = Session.objects.filter(
                expire_date__gte=timezone.now())
            [
                session.delete() for session in unexpired_sessions
                if str(user.pk) == session.get_decoded().get('_auth_user_id')
            ]
            result = '0'
    return JsonResponse({'status': result})


def reset(request):
    # 6.重設密碼
    result = '1'
    try:
        if request.method == 'POST':
            token = request.POST.get('token', '')
            password = request.POST.get('password', '')
            if token and password:
                s = Session.objects.get(pk=token).get_decoded()
                user = Patient.objects.get(id=s['_auth_user_id'])
                user.set_password(password)
                user.save()
                unexpired_sessions = Session.objects.filter(
                    expire_date__gte=timezone.now())
                [
                    session.delete() for session in unexpired_sessions
                    if str(user.pk) == session.get_decoded().get('_auth_user_id')
                ]
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def privacy_policy(request):
    # 13.隱私權聲明 FBLogin
    result = '1'
    try:
        if request.method == 'POST':
            result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def rcheck(request):
    # 38.註冊確認
    result = '1'
    try:
        if request.method == 'GET':
            Patient.objects.get(username=request.GET['account'])
            result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def personal_info(request):
    # 7.個人資訊設定
    result = '1'
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        if request.method == 'PATCH':
            patch = MultiPartParser(request.META, request,
                                    request.upload_handlers).parse()[0].dict()
            f = PersonalInfoForm(patch)
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                for i in filtered:
                    setattr(user, i, data[i])
                if 'email' in filtered:
                    unexpired_sessions = Session.objects.filter(
                        expire_date__gte=timezone.now())
                    [
                        session.delete() for session in unexpired_sessions
                        if str(user.pk) == session.get_decoded().get('_auth_user_id')
                    ]
                    user.is_active = False
                user.save()
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})
