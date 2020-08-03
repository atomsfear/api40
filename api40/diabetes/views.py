from django.http import JsonResponse
from diabetes.models import Patient, EmailAuth, Default, Setting, Medical, Drug, A1cs
from diabetes.forms import RegisterForm, PersonalInfoForm, PersonalDefaultForm, SettingForm, MedicalForm, DrugForm, A1csForm
from django.contrib import auth as Auth
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone
import random
import string
import time
from collections import OrderedDict
import json
# Create your views here.


def register(request):
    # 1.註冊
    result = '1'
    try:
        if request.method == 'POST':
            f = RegisterForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                account = f.cleaned_data['account']
                phone = f.cleaned_data['phone']
                email = f.cleaned_data['email']
                password = f.cleaned_data['password']
                user = Patient.objects.create(
                    username=account, email=email, phone=phone, is_active=False)
                user.set_password(password)
                Default.objects.create(
                    id=user.pk, user_id=user.pk, patient=user)
                Setting.objects.create(
                    id=user.pk, user_id=user.pk, patient=user)
                Medical.objects.create(
                    id=user.pk, user_id=user.pk, patient=user)
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
            data = json.loads(request.body.decode("utf-8"))
            account = data['account'] if 'account' in data else ''
            password = data['password'] if 'password' in data else ''
            verified = False
            if account and password:
                user = Auth.authenticate(username=account, password=password)
                if user is not None:
                    verified = True
                else:
                    email = Patient.objects.filter(email=account)
                    if email:
                        user = Auth.authenticate(
                            username=email[0].username, password=password)
                        if user is not None:
                            verified = True
                    else:
                        phone = Patient.objects.filter(phone=account)
                        if phone:
                            user = Auth.authenticate(
                                username=phone[0].username, password=password)
                            if user is not None:
                                verified = True
            if verified:
                if user.is_active:
                    request.session.create()
                    Auth.login(request, user)
                    if "phone" in locals():
                        user = phone[0]
                    elif "email" in locals():
                        user = email[0]
                    else:
                        user = Patient.objects.get(username=account)
                    user.login_times += 1
                    user.save()
                    result = '0'
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
            data = json.loads(request.body.decode("utf-8"))
            phone = data['phone'] if 'phone' in data else ''
            email = data['email'] if 'email' in data else ''
            if phone or email:
                if email:
                    try:
                        user = Patient.objects.get(email=email)
                    except Patient.DoesNotExist:
                        user = None
                    if user is None:
                        user = Patient.objects.get(phone=phone)
                        if user.email in ['', None]:
                            raise Exception
                else:
                    user = Patient.objects.get(phone=phone)
                    if user.email in ['', None]:
                        raise Exception
                if not user.is_active:
                    duration = 3600
                    code = ''.join([random.choice(
                        string.ascii_letters + string.digits) for i in range(25)])
                    EmailAuth.objects.filter(patient=user).delete()
                    EmailAuth.objects.create(code=code, end_time=int(
                        time.time()+duration), patient=user)
                    title = "meter123.com 信箱驗證碼"
                    msg = 'code：' + code + '\nExpire：' + \
                        time.strftime('%Y-%m-%d %H:%M:%S %z',
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
            data = json.loads(request.body.decode("utf-8"))
            code = data['code'] if 'code' in data else ''
            phone = data['phone'] if 'phone' in data else ''
            email = data['email'] if 'email' in data else ''
            if code and phone:
                verify = EmailAuth.objects.get(code=code)
                user = verify.patient
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
                    user.verified = '1'
                    user.save()
                    verify.delete()
                    result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def forgot(request):
    # 5.忘記密碼
    result = '1'
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode("utf-8"))
            email = data['email'] if 'email' in data else ''
            phone = data['phone'] if 'phone' in data else ''
            if phone or email:
                if email:
                    try:
                        user = Patient.objects.get(email=email)
                    except Patient.DoesNotExist:
                        user = None
                    if user is None:
                        user = Patient.objects.get(phone=phone)
                        if user.email in ['', None]:
                            raise Exception
                else:
                    user = Patient.objects.get(phone=phone)
                    if user.email in ['', None]:
                        raise Exception
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
    except:
        pass
    return JsonResponse({'status': result})


def reset(request):
    # 6.重設密碼
    result = '1'
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode("utf-8"))
            token = data['token']
            password = data['password']
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
    # 7.個人資訊設定，12.個人資訊
    result = {'status': '1'}
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 7.個人資訊設定
        if request.method == 'PATCH':
            f = PersonalInfoForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    if 'email' in filtered:
                        for i in filtered:
                            setattr(user, i, filtered[i])
                        unexpired_sessions = Session.objects.filter(
                            expire_date__gte=timezone.now())
                        [
                            session.delete() for session in unexpired_sessions
                            if str(user.pk) == session.get_decoded().get('_auth_user_id')
                        ]
                        user.is_active = False
                        user.verified = '0'
                    user.save()
                result = {'status': '0'}
        # 12.個人資訊
        if request.method == 'GET':
            result = OrderedDict([('status', '0')])
            result['user'] = OrderedDict([
                ("id", user.pk),
                ("name", user.name),
                ("account", user.username),
                ("email", user.email),
                ("phone", user.phone),
                ("fb_id", user.fb_id),
                ("status", user.status),
                ("group", user.group),
                ("birthday", user.birthday),
                ("height", None if user.height is None else float(user.height)),
                ("weight", None if user.weight is None else float(user.weight)),
                ("gender", None if user.gender is None else int(user.gender)),
                ("address", user.address),
                ("unread_records", [
                    int(user.unread_records_one),
                    user.unread_records_two,
                    int(user.unread_records_three)
                ]),
                ("verified", int(user.verified)),
                ("private_policy", int(user.privacy_policy)),
                ("must_change_password", int(user.must_change_password)),
                ("fcm_id", user.fcm_id),
                ("badge", int(user.badge)),
                ("login_times", int(user.login_times)),
                ("created_at", str(user.created_at.replace(
                    tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                ("updated_at", str(user.updated_at.replace(
                    tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                ("default", OrderedDict([
                    ("id", int(user.default.id)),
                    ("user_id", int(user.default.user_id)),
                    ("sugar_delta_max", None if user.default.sugar_delta_max is None else int(
                        user.default.sugar_delta_max)),
                    ("sugar_delta_min", None if user.default.sugar_delta_min is None else int(
                        user.default.sugar_delta_min)),
                    ("sugar_morning_max", None if user.default.sugar_morning_max is None else int(
                        user.default.sugar_morning_max)),
                    ("sugar_morning_min", None if user.default.sugar_morning_min is None else int(
                        user.default.sugar_morning_min)),
                    ("sugar_evening_max", None if user.default.sugar_evening_max is None else int(
                        user.default.sugar_evening_max)),
                    ("sugar_evening_min", None if user.default.sugar_evening_min is None else int(
                        user.default.sugar_evening_min)),
                    ("sugar_before_max", None if user.default.sugar_before_max is None else int(
                        user.default.sugar_before_max)),
                    ("sugar_before_min", None if user.default.sugar_before_min is None else int(
                        user.default.sugar_before_min)),
                    ("sugar_after_max", None if user.default.sugar_after_max is None else int(
                        user.default.sugar_after_max)),
                    ("sugar_after_min", None if user.default.sugar_after_min is None else int(
                        user.default.sugar_after_min)),
                    ("systolic_max", None if user.default.systolic_max is None else int(
                        user.default.systolic_max)),
                    ("systolic_min", None if user.default.systolic_min is None else int(
                        user.default.systolic_min)),
                    ("diastolic_max", None if user.default.diastolic_max is None else int(
                        user.default.diastolic_max)),
                    ("diastolic_min", None if user.default.diastolic_min is None else int(
                        user.default.diastolic_min)),
                    ("pulse_max", None if user.default.pulse_max is None else int(
                        user.default.pulse_max)),
                    ("pulse_min", None if user.default.pulse_min is None else int(
                        user.default.pulse_min)),
                    ("weight_max", None if user.default.weight_max is None else int(
                        user.default.weight_max)),
                    ("weight_min", None if user.default.weight_min is None else int(
                        user.default.weight_min)),
                    ("bmi_max", None if user.default.bmi_max is None else int(
                        user.default.bmi_max)),
                    ("bmi_min", None if user.default.bmi_min is None else int(
                        user.default.bmi_min)),
                    ("body_fat_max", None if user.default.body_fat_max is None else int(
                        user.default.body_fat_max)),
                    ("body_fat_min", None if user.default.body_fat_min is None else int(
                        user.default.body_fat_min)),
                    ("created_at", str(user.default.created_at.replace(
                        tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                    ("updated_at", str(user.default.updated_at.replace(
                        tzinfo=timezone.utc).astimezone(tz=None))[:19])
                ])),
                ("setting", OrderedDict([
                    ("id", int(user.setting.id)),
                    ("user_id", int(user.setting.user_id)),
                    ("after_recording", int(user.setting.after_recording)),
                    ("no_recording_for_a_day", int(
                        user.setting.no_recording_for_a_day)),
                    ("over_max_or_under_min", int(
                        user.setting.over_max_or_under_min)),
                    ("after_meal", int(user.setting.after_meal)),
                    ("unit_of_sugar", int(user.setting.unit_of_sugar)),
                    ("unit_of_weight", int(user.setting.unit_of_weight)),
                    ("unit_of_height", int(user.setting.unit_of_height)),
                    ("created_at", str(user.setting.created_at.replace(
                        tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                    ("updated_at", str(user.setting.updated_at.replace(
                        tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                ]))
            ])
    except:
        pass
    return JsonResponse(result)


def default(request):
    # 11.個人預設值
    result = '1'
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        if request.method == 'PATCH':
            f = PersonalDefaultForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user.default, i, filtered[i])
                    user.default.save()
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def setting(request):
    # 35.個人設定
    result = '1'
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        if request.method == 'PATCH':
            f = SettingForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user.setting, i, filtered[i])
                    user.setting.save()
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def badge(request):
    # 39.更新badge
    result = '1'
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        if request.method == 'PUT':
            put = json.loads(request.body.decode("utf-8"))
            if 'badge' in put:
                user.badge = put['badge']
                user.save()
                result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def medical(request):
    # 30. 就醫資訊，31. 更新就醫資訊
    result = {'status': '1'}
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 30. 就醫資訊
        if request.method == 'GET':
            result = OrderedDict([('status', '0')])
            result['medical_info'] = OrderedDict([
                ("id", int(user.medical.id)),
                ("user_id", int(user.medical.user_id)),
                ("diabetes_type", int(user.medical.diabetes_type)),
                ("oad", int(user.medical.oad)),
                ("insulin", int(user.medical.insulin)),
                ("anti_hypertensives", int(user.medical.anti_hypertensives)),
                ("created_at", str(user.medical.created_at.replace(
                    tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                ("updated_at", str(user.medical.updated_at.replace(
                    tzinfo=timezone.utc).astimezone(tz=None))[:19])
            ])
        # 31. 更新就醫資訊
        if request.method == 'PATCH':
            f = MedicalForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user.medical, i, filtered[i])
                    user.medical.save()
                result = {'status': '0'}
    except:
        pass
    return JsonResponse(result)


def a1c(request):
    # 32.糖化血色素，33.送糖化血色素，34.刪除糖化血色素
    result = {'status': '1'}
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 32.糖化血色素
        if request.method == 'GET':
            result = OrderedDict([
                ("status", '0'),
                ("a1cs", [
                    OrderedDict([
                        ("id", a1c.id),
                        ("user_id", int(a1c.user_id)),
                        ("a1c", int(a1c.a1c)),
                        ("recorded_at", str(a1c.recorded_at.replace(
                            tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                        ("created_at", str(a1c.created_at.replace(
                            tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                        ("updated_at", str(a1c.updated_at.replace(
                            tzinfo=timezone.utc).astimezone(tz=None))[:19])
                    ]) for a1c in user.a1cs_set.all()
                ])
            ])
        # 33.送糖化血色素
        if request.method == 'POST':
            f = A1csForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    a1c = A1cs.objects.create(user_id=user.pk, patient=user)
                    for i in filtered:
                        setattr(a1c, i, filtered[i])
                    a1c.save()
                result = {'status': '0'}
        # 34.刪除糖化血色素
        if request.method == 'DELETE':
            data = json.loads(request.body.decode("utf-8"))
            if all([user.a1cs_set.filter(id=ids).exists() for ids in data["ids"]]):
                [
                    user.a1cs_set.get(id=ids).delete() for ids in data["ids"]
                ]
                result = {'status': '0'}
    except:
        pass
    return JsonResponse(result)


def drug_used(request):
    # 41.藥物資訊，42.上傳藥物資訊，43.刪除藥物資訊
    result = {'status': '1'}
    try:
        s = Session.objects.get(pk=request.headers.get(
            'Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 41.藥物資訊
        if request.method == 'GET':
            result = OrderedDict([
                ("status", '0'),
                ("drug_used", [
                    OrderedDict([
                        ("id", drug.id),
                        ("user_id", int(drug.user_id)),
                        ("type", None if drug.type is None else int(drug.type)),
                        ("name", drug.name),
                        ("recorded_at", str(drug.recorded_at.replace(
                            tzinfo=timezone.utc).astimezone(tz=None))[:19])
                    ]) for drug in user.drug_set.filter(type=request.GET['type'])
                ])
            ])
        # 42.上傳藥物資訊
        if request.method == 'POST':
            f = DrugForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    drug = Drug.objects.create(user_id=user.pk, patient=user)
                    for i in filtered:
                        setattr(drug, i, filtered[i])
                    drug.save()
                result = {'status': '0'}
        # 43.刪除藥物資訊
        if request.method == 'DELETE':
            data = json.loads(request.body.decode("utf-8"))
            if all([user.drug_set.filter(id=ids).exists() for ids in data["ids"]]):
                [
                    user.drug_set.get(id=ids).delete() for ids in data["ids"]
                ]
                result = {'status': '0'}
    except:
        pass
    return JsonResponse(result)


def news(request):
    # 29. 最新消息
    result = {'status': '1'}
    try:
        if request.method == 'GET':
            s = Session.objects.get(pk=request.headers.get(
                'Authorization', '')).get_decoded()
            user = Patient.objects.get(id=s['_auth_user_id'])
            result = OrderedDict([
                ('status', '0'),
                ('news', [])
            ])
    except:
        pass
    return JsonResponse(result)


def share(request, relation_type=3):
    # 23.分享，24.查看分享（含自己分享出去的）
    result = {'status': '1'}
    try:
        # 23.分享
        if request.method == 'POST':
            pass
        # 24.查看分享（含自己分享出去的）
        if request.method == 'GET':
            s = Session.objects.get(pk=request.headers.get(
                'Authorization', '')).get_decoded()
            user = Patient.objects.get(id=s['_auth_user_id'])
            if relation_type not in [0, 1, 2]:
                raise Exception
            result = OrderedDict([
                ('status', '0'),
                ('records', [])
            ])
    except:
        pass
    return JsonResponse(result)
