from django.http import JsonResponse
from diabetes.models import Patient, EmailAuth, Default, Setting, Medical, Drug, A1cs, userblood, userweight, userbloodsugar, dietmod, care, notificationmod, friendmod, receivemod
from diabetes.forms import RegisterForm, PersonalInfoForm, PersonalDefaultForm, SettingForm, MedicalForm, DrugForm, A1csForm, UbloodForm, UweightForm, UbloodsugarForm, DietForm, CareForm, NotificationForm, receiveForm
from django.contrib import auth as Auth
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone
from django.http.multipartparser import MultiPartParser
import random
import string
import time
import datetime
from collections import OrderedDict
import json
# Create your views here.


def register(request):
    # 1.註冊
    result = '1'
    try:
        if request.method == 'POST':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            print(data)
            f = RegisterForm(data)
            if f.is_valid():
                print(f.cleaned_data)
                account = f.cleaned_data['account']
                phone = f.cleaned_data['phone']
                email = f.cleaned_data['email']
                password = f.cleaned_data['password']
                user = Patient.objects.create(username=account,
                                              email=email,
                                              phone=phone)
                user.set_password(password)
                Default.objects.create(id=user.pk,
                                       user_id=user.pk,
                                       patient=user)
                Setting.objects.create(id=user.pk,
                                       user_id=user.pk,
                                       patient=user)
                Medical.objects.create(id=user.pk,
                                       user_id=user.pk,
                                       patient=user)
                user.invite_code = ''.join([
                    random.choice(string.ascii_letters + string.digits)
                    for i in range(6)
                ])
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
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
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
                        user = Auth.authenticate(username=email[0].username,
                                                 password=password)
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
        return JsonResponse({
            'status': result,
            'token': request.session.session_key
        })
    else:
        return JsonResponse({'status': result})


def send(request):
    # 3.發送驗證碼
    result = '1'
    try:
        if request.method == 'POST':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            print(data)
            duration = 3600
            code = ''.join([
                random.choice(string.ascii_letters + string.digits)
                for i in range(5)
            ])
            EmailAuth.objects.create(code=code,
                                     end_time=int(time.time() + duration))
            title = "meter123.com 信箱驗證碼"
            msg = 'code：' + code + '\nExpire：' + \
                time.strftime('%Y-%m-%d %H:%M:%S %z',
                              time.localtime(time.time()+duration))
            email_from = 'secretclubonly007@gmail.com'
            reciever = [data['email']]
            send_mail(title, msg, email_from, reciever, fail_silently=False)
            result = '0'
    except:
        pass
    return JsonResponse({'status': result})


def vcheck(request):
    # 4.檢查驗證碼
    result = '1'
    try:
        if request.method == 'POST':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            verify = EmailAuth.objects.get(code=data['code'])
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
                new_password = ''.join([
                    random.choice(string.ascii_letters + string.digits)
                    for i in range(12)
                ])
                title = "meter123.com 新密碼"
                msg = '請使用新密碼登入！！\n新密碼：' + new_password
                email_from = 'secretclubonly007@gmail.com'
                reciever = [user.email]
                send_mail(title,
                          msg,
                          email_from,
                          reciever,
                          fail_silently=False)
                user.set_password(new_password)
                user.save()
                unexpired_sessions = Session.objects.filter(
                    expire_date__gte=timezone.now())
                [
                    session.delete() for session in unexpired_sessions if str(
                        user.pk) == session.get_decoded().get('_auth_user_id')
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
    result = '0'
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
    # try:
    if 1:
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')[7:]).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 7.個人資訊設定
        if request.method == 'PATCH':
            f = PersonalInfoForm(json.loads(request.body.decode("utf-8")))
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user, i, filtered[i])
                    if 'email' in filtered:
                        unexpired_sessions = Session.objects.filter(
                            expire_date__gte=timezone.now())
                        [
                            session.delete() for session in unexpired_sessions
                            if str(user.pk) == session.get_decoded().get(
                                '_auth_user_id')
                        ]
                        user.is_active = False
                        user.verified = '0'
                    user.save()
                result = {'status': '0'}
        # 12.個人資訊
        if request.method == 'GET':
            result = OrderedDict([('status', '0')])
            result['user'] = OrderedDict([
                ("id", user.pk), ("name", user.name),
                ("account", user.username), ("email", user.email),
                ("phone", user.phone), ("fb_id", user.fb_id),
                ("status", user.status), ("group", user.group),
                ("birthday", user.birthday),
                ("height",
                 None if user.height is None else float(user.height)),
                ("weight",
                 None if user.weight is None else float(user.weight)),
                ("gender", None if user.gender is None else int(user.gender)),
                ("address", user.address),
                ("unread_records", [
                    int(user.unread_records_one), user.unread_records_two,
                    int(user.unread_records_three)
                ]), ("verified", int(user.verified)),
                ("private_policy", int(user.privacy_policy)),
                ("must_change_password", int(user.must_change_password)),
                ("fcm_id", user.fcm_id), ("badge", int(user.badge)),
                ("login_times", int(user.login_times)),
                ("created_at",
                 str(
                     user.created_at.replace(tzinfo=timezone.utc).astimezone(
                         tz=None))[:19]),
                ("updated_at",
                 str(
                     user.updated_at.replace(tzinfo=timezone.utc).astimezone(
                         tz=None))[:19]),
                ("default",
                 OrderedDict([
                     ("id", int(user.default.id)),
                     ("user_id", int(user.default.user_id)),
                     ("sugar_delta_max",
                      None if user.default.sugar_delta_max is None else int(
                          user.default.sugar_delta_max)),
                     ("sugar_delta_min",
                      None if user.default.sugar_delta_min is None else int(
                          user.default.sugar_delta_min)),
                     ("sugar_morning_max",
                      None if user.default.sugar_morning_max is None else int(
                          user.default.sugar_morning_max)),
                     ("sugar_morning_min",
                      None if user.default.sugar_morning_min is None else int(
                          user.default.sugar_morning_min)),
                     ("sugar_evening_max",
                      None if user.default.sugar_evening_max is None else int(
                          user.default.sugar_evening_max)),
                     ("sugar_evening_min",
                      None if user.default.sugar_evening_min is None else int(
                          user.default.sugar_evening_min)),
                     ("sugar_before_max",
                      None if user.default.sugar_before_max is None else int(
                          user.default.sugar_before_max)),
                     ("sugar_before_min",
                      None if user.default.sugar_before_min is None else int(
                          user.default.sugar_before_min)),
                     ("sugar_after_max",
                      None if user.default.sugar_after_max is None else int(
                          user.default.sugar_after_max)),
                     ("sugar_after_min",
                      None if user.default.sugar_after_min is None else int(
                          user.default.sugar_after_min)),
                     ("systolic_max", None if user.default.systolic_max is None
                      else int(user.default.systolic_max)),
                     ("systolic_min", None if user.default.systolic_min is None
                      else int(user.default.systolic_min)),
                     ("diastolic_max",
                      None if user.default.diastolic_max is None else int(
                          user.default.diastolic_max)),
                     ("diastolic_min",
                      None if user.default.diastolic_min is None else int(
                          user.default.diastolic_min)),
                     ("pulse_max", None if user.default.pulse_max is None else
                      int(user.default.pulse_max)),
                     ("pulse_min", None if user.default.pulse_min is None else
                      int(user.default.pulse_min)),
                     ("weight_max", None if user.default.weight_max is None
                      else int(user.default.weight_max)),
                     ("weight_min", None if user.default.weight_min is None
                      else int(user.default.weight_min)),
                     ("bmi_max", None if user.default.bmi_max is None else int(
                         user.default.bmi_max)),
                     ("bmi_min", None if user.default.bmi_min is None else int(
                         user.default.bmi_min)),
                     ("body_fat_max", None if user.default.body_fat_max is None
                      else int(user.default.body_fat_max)),
                     ("body_fat_min", None if user.default.body_fat_min is None
                      else int(user.default.body_fat_min)),
                     ("created_at",
                      str(
                          user.default.created_at.replace(
                              tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                     ("updated_at",
                      str(
                          user.default.updated_at.replace(
                              tzinfo=timezone.utc).astimezone(tz=None))[:19])
                 ])),
                ("setting",
                 OrderedDict([
                     ("id", int(user.setting.id)),
                     ("user_id", int(user.setting.user_id)),
                     ("after_recording", int(user.setting.after_recording)),
                     ("no_recording_for_a_day",
                      int(user.setting.no_recording_for_a_day)),
                     ("over_max_or_under_min",
                      int(user.setting.over_max_or_under_min)),
                     ("after_meal", int(user.setting.after_meal)),
                     ("unit_of_sugar", int(user.setting.unit_of_sugar)),
                     ("unit_of_weight", int(user.setting.unit_of_weight)),
                     ("unit_of_height", int(user.setting.unit_of_height)),
                     ("created_at",
                      str(
                          user.setting.created_at.replace(
                              tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                     ("updated_at",
                      str(
                          user.setting.updated_at.replace(
                              tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                 ]))
            ])
    # except:
    #     pass
    return JsonResponse(result)


def default(request):
    # 11.個人預設值
    result = '1'
    try:
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
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
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
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
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
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
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
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
                ("created_at",
                 str(
                     user.medical.created_at.replace(
                         tzinfo=timezone.utc).astimezone(tz=None))[:19]),
                ("updated_at",
                 str(
                     user.medical.updated_at.replace(
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
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 32.糖化血色素
        if request.method == 'GET':
            result = OrderedDict([
                ("status", '0'),
                ("a1cs", [
                    OrderedDict([("id", a1c.id), ("user_id", int(a1c.user_id)),
                                 ("a1c", int(a1c.a1c)),
                                 ("recorded_at",
                                  str(
                                      a1c.recorded_at.replace(
                                          tzinfo=timezone.utc).astimezone(
                                              tz=None))[:19]),
                                 ("created_at",
                                  str(
                                      a1c.created_at.replace(
                                          tzinfo=timezone.utc).astimezone(
                                              tz=None))[:19]),
                                 ("updated_at",
                                  str(
                                      a1c.updated_at.replace(
                                          tzinfo=timezone.utc).astimezone(
                                              tz=None))[:19])])
                    for a1c in user.a1cs_set.all()
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
            if all(
                [user.a1cs_set.filter(id=ids).exists()
                 for ids in data["ids"]]):
                [user.a1cs_set.get(id=ids).delete() for ids in data["ids"]]
                result = {'status': '0'}
    except:
        pass
    return JsonResponse(result)


def drug_used(request):
    # 41.藥物資訊，42.上傳藥物資訊，43.刪除藥物資訊
    result = {'status': '1'}
    try:
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        # 41.藥物資訊
        if request.method == 'GET':
            result = OrderedDict([
                ("status", '0'),
                ("drug_used", [
                    OrderedDict([
                        ("id", drug.id), ("user_id", int(drug.user_id)),
                        ("type",
                         None if drug.type is None else int(drug.type)),
                        ("name", drug.name),
                        ("recorded_at",
                         str(
                             drug.recorded_at.replace(
                                 tzinfo=timezone.utc).astimezone(
                                     tz=None))[:19])
                    ])
                    for drug in user.drug_set.filter(type=request.GET['type'])
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
            if all(
                [user.drug_set.filter(id=ids).exists()
                 for ids in data["ids"]]):
                [user.drug_set.get(id=ids).delete() for ids in data["ids"]]
                result = {'status': '0'}
    except:
        pass
    return JsonResponse(result)


def news(request):
    # 29. 最新消息
    result = {'status': '1'}
    try:
        if request.method == 'GET':
            s = Session.objects.get(
                pk=request.headers.get('Authorization', '')).get_decoded()
            user = Patient.objects.get(id=s['_auth_user_id'])
            result = OrderedDict([('status', '0'), ('news', [])])
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
            s = Session.objects.get(
                pk=request.headers.get('Authorization', '')).get_decoded()
            user = Patient.objects.get(id=s['_auth_user_id'])
            if relation_type not in [0, 1, 2]:
                raise Exception
            result = OrderedDict([('status', '0'), ('records', [])])
    except:
        pass
    return JsonResponse(result)


def ublood(request):  #血压
    result = '1'
    if request.method == 'POST':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()  #解密
        user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
        form = UbloodForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            systolic = form.cleaned_data['systolic']
            diastolic = form.cleaned_data['diastolic']
            pulse = form.cleaned_data['pulse']
            blood = userblood.objects.create(systolic=systolic,
                                             diastolic=diastolic,
                                             pulse=pulse,
                                             patient=user)
            # blood.systolic=form.cleaned_data['systolic']
            # userblood.diastolic=form.cleaned_data['diastolic']
            # user.userblood.pulse=form.cleaned_data['pulse']
            blood.save()
            result = '0'

    else:
        # form = UbloodForm()
        # return render(request, 'ublood.html',{'form': form})
        return JsonResponse({'status': result})
    return JsonResponse({'status': result})


def uweight(request):  #体重
    result = '1'
    # try:
    if True:
        if request.method == 'POST':
            s = Session.objects.get(
                pk=request.headers.get('Authorization', '')).get_decoded()  #解密
            user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
            form = UweightForm(json.loads(request.body.decode("utf-8")))
            if form.is_valid():
                weight = form.cleaned_data['weight']
                body_fat = form.cleaned_data['body_fat']
                bmi = form.cleaned_data['bmi']
                iweight = userweight.objects.create(weight=weight,
                                                    body_fat=body_fat,
                                                    bmi=bmi,
                                                    patient=user)
                # user.userweight.weight=form.cleaned_data['weight']
                # user.userweight.body_fat=form.cleaned_data['body_fat']
                # user.userweight.bmi=form.cleaned_data['bmi']
                # recorded_at=form.cleaned_data['recorded_at']
                iweight.save()
                # user.userweight.save()
                result = '0'
    return JsonResponse({'status': result})


def ubloodsugar(request):  #血糖
    result = '1'
    if request.method == 'POST':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()  #解密
        user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
        form = UbloodsugarForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            sugar = form.cleaned_data['sugar']
            timeperiod = form.cleaned_data['timeperiod']
            # user.userbloodsugar.sugar=form.cleaned_data['sugar']
            # user.userbloodsugar.timeperiod=form.cleaned_data['timeperiod']
            # recorded_at=form.cleaned_data['recorded_at']
            isugar = userbloodsugar.objects.create(sugar=sugar,
                                                   timeperiod=timeperiod,
                                                   patient=user)
            isugar.save()
            # user.userbloodsugar.save()
            result = '0'
        # form = UbloodsugarForm()
        # return render(request, 'usugar.html',{'form': form})
    return JsonResponse({'status': result})


def userdiet(request):  #饮食日记
    result = '1'
    if request.method == 'POST':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()  #解密
        user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
        form = DietForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            description = form.cleaned_data['description']
            meal = form.cleaned_data['meal']
            tag = form.cleaned_data['tag']
            image = form.cleaned_data['image']
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            idiet = dietmod.objects.create(description=description,
                                           meal=meal,
                                           tag=tag,
                                           image=image,
                                           lat=lat,
                                           lng=lng,
                                           patient=user)
            idiet.save()
            result = '0'
    return JsonResponse({
        'status':
        result,
        'image_url':
        "http://211.23.17.100:3001/diet_1_2017-10-12_11:11:11_0"
    })


def diary(request):
    result = {'status': '1'}
    s = Session.objects.get(
        pk=request.headers.get('Authorization', '')).get_decoded()
    user = Patient.objects.get(id=s['_auth_user_id'])
    if request.method == 'GET':
        try:
            da = request.GET['date']
        except:
            da = str(datetime.date.today())

        bp = [
            i.id for i in user.userblood_set.all()
            if str(i.update_time)[:10] == da
        ]
        we = [
            i.id for i in user.userweight_set.all()
            if str(i.update_time)[:10] == da
        ]
        bs = [
            i.id for i in user.userbloodsugar_set.all()
            if str(i.update_time)[:10] == da
        ]
        di = [
            i.id for i in user.dietmod_set.all()
            if str(i.update_time)[:10] == da
        ]
        mm = max([len(bp), len(we), len(bs), len(di)])

        result = OrderedDict([('status', '0')])

        result['diary'] = []
        for i in range(mm):
            if i < len(bp):
                bp1 = bp[i]
                r = userblood.objects.get(id=bp1)
                result['diary'].append(
                    OrderedDict([("blood_pressure",
                                  OrderedDict([
                                      ("id", r.id),
                                      ("user_id", user.pk),
                                      ("systolic", r.systolic),
                                      ("diastolic", r.diastolic),
                                      ("pulse", r.pulse),
                                      ("recorded_at",
                                       str(
                                           r.update_time.replace(
                                               tzinfo=timezone.utc).astimezone(
                                                   tz=None))[:19]),
                                      ("type", "blood_pressure"),
                                  ]))]))
            if i < len(we):
                we1 = we[i]
                r = userweight.objects.get(id=we1)
                result['diary'].append(
                    OrderedDict([("weight",
                                  OrderedDict([
                                      ("id", r.id),
                                      ("user_id", user.pk),
                                      ("weight", r.weight),
                                      ("body_fat", r.body_fat),
                                      ("bmi", r.bmi),
                                      ("recorded_at",
                                       str(
                                           r.update_time.replace(
                                               tzinfo=timezone.utc).astimezone(
                                                   tz=None))[:19]),
                                      ("type", "weight"),
                                  ]))]))
            if i < len(bs):
                bs1 = bs[i]
                r = userbloodsugar.objects.get(id=bs1)
                result['diary'].append(
                    OrderedDict([
                        ("blood_sugar",
                         OrderedDict([
                             ("id", user.userbloodsugar_set.last().id),
                             ("user_id", user.pk),
                             ("sugar", user.userbloodsugar_set.last().sugar),
                             ("timeperiod",
                              user.userbloodsugar_set.last().timeperiod),
                             ("recorded_at",
                              str(
                                  r.update_time.replace(
                                      tzinfo=timezone.utc).astimezone(
                                          tz=None))[:19]),
                             ("type", "blood_sugar"),
                         ]))
                    ]))
            if i < len(di):
                di1 = di[i]
                r = dietmod.objects.get(id=di1)
                result['diary'].append(
                    OrderedDict([
                        ("location",
                         OrderedDict([
                             ("id", user.dietmod_set.last().id),
                             ("user_id", user.pk),
                             ("description",
                              user.dietmod_set.last().description),
                             ("meal", user.dietmod_set.last().meal),
                             ("tag", user.dietmod_set.last().tag),
                             ("image", user.dietmod_set.last().image),
                             ("diet",
                              OrderedDict([
                                  ("lat", user.dietmod_set.last().lat),
                                  ("lng", user.dietmod_set.last().lng),
                              ])),
                             ("recorded_at",
                              str(
                                  r.update_time.replace(
                                      tzinfo=timezone.utc).astimezone(
                                          tz=None))[:19]),
                             ("type", "diet"),
                             ("reply", "hello"),
                         ]))
                    ]))
    return JsonResponse(result)


def friendcode(request):
    result = '1'
    s = Session.objects.get(
        pk=request.headers.get('Authorization', '')).get_decoded()
    user = Patient.objects.get(id=s['_auth_user_id'])
    if request.method == 'GET':
        fcode = user.invite_code
        result = '0'
    return JsonResponse({'status': result, 'invite_code': fcode})


# def friendlist(request):
#     result = {'status': '1'}
#     s = Session.objects.get(pk=request.headers.get(
#             'Authorization', '')).get_decoded()
#     user = Patient.objects.get(id=s['_auth_user_id'])
#     if request.method == 'GET':
#         result = OrderedDict([('status', '0')])

# def usercare(request):
#     result = {'status': '1'}
#     s = Session.objects.get(pk=request.headers.get(
#             'Authorization', '')).get_decoded()
#     user = Patient.objects.get(id=s['_auth_user_id'])
#     if request.method == 'GET':
#         result = OrderedDict([('status', '0')])


def userrecords(request):  #上一笔资料
    result = {'status': '1'}
    s = Session.objects.get(
        pk=request.headers.get('Authorization', '')).get_decoded()
    user = Patient.objects.get(id=s['_auth_user_id'])
    if len(user.userblood_set.all()) > 1:
        blood = user.userblood_set.all()[len(user.userblood_set.all()) - 2]
    elif len(user.userblood_set.all()) == 1:
        blood = user.userblood_set.all()[len(user.userblood_set.all()) - 1]
    else:
        blood = None
    if len(user.userweight_set.all()) > 1:
        weight = user.userweight_set.all()[len(user.userweight_set.all()) - 2]
    elif len(user.userweight_set.all()) == 1:
        weight = user.userweight_set.all()[0]
    else:
        weight = None
    if len(user.userbloodsugar_set.all()) > 1:
        bloodsugar = user.userbloodsugar_set.all()[
            len(user.userbloodsugar_set.all()) - 2]
    elif len(user.userbloodsugar_set.all()) == 1:
        bloodsugar = user.userbloodsugar_set.all()[
            len(user.userbloodsugar_set.all()) - 1]
    else:
        bloodsugar = None
    print("-------------------")
    print(weight)
    if request.method == 'POST':
        result = OrderedDict([('status', '0')])
        result['records'] = OrderedDict([
            ("blood_pressure",
             OrderedDict([
                 ("id", blood.id),
                 ("user_id", user.pk),
                 ("systolic", blood.systolic),
                 ("diastolic", blood.diastolic),
                 ("pulse", blood.pulse),
                 ("recorded_at", str(blood.update_time)),
                 ("type", "blood_pressure"),
             ])),
            ("weight",
             OrderedDict([
                 ("id", weight.id),
                 ("user_id", user.pk),
                 ("weight", weight.weight),
                 ("body_fat", weight.body_fat),
                 ("bmi", weight.bmi),
                 ("recorded_at", str(weight.update_time)),
                 ("type", "weight"),
             ])),
            ("blood_sugar",
             OrderedDict([
                 ("id", bloodsugar.id),
                 ("user_id", user.pk),
                 ("sugar", bloodsugar.sugar),
                 ("timeperiod", bloodsugar.timeperiod),
                 ("recorded_at", str(bloodsugar.update_time)),
                 ("type", "blood_sugar"),
             ])),
        ])
    if request.method == 'DELETE':
        data = json.loads(request.body.decode("utf-8"))
        if all([
                user.userbloodsugar_set.filter(id=ids).exists()
                for ids in data["blood_sugars"]
        ]):
            [
                user.userbloodsugar_set.get(id=ids).delete()
                for ids in data["blood_sugars"]
            ]
        if all([
                user.userblood_set.filter(id=ids).exists()
                for ids in data["blood_pressures"]
        ]):
            [
                user.userblood_set.get(id=ids).delete()
                for ids in data["blood_pressures"]
            ]
        if all([
                user.userweight_set.filter(id=ids).exists()
                for ids in data["weights"]
        ]):
            [
                user.userweight_set.get(id=ids).delete()
                for ids in data["weights"]
            ]
        result = {'status': '0'}
    return JsonResponse(result)


def usercare(request):  #发送关怀资讯
    result = {'status': '1'}
    if request.method == 'POST':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
        form = CareForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            message = form.cleaned_data['message']
            icare = care.objects.create(message=message, patient=user)
            icare.save()
            result = {'status': '0'}
        return JsonResponse(result)
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        result = OrderedDict([('status', '0')])
        result['cares'] = [
            OrderedDict([
                ("id", care.id),
                ("user_id", user.pk),
                ("message", care.message),
                ("member_id", "1"),
                ("reply_id", "1"),
                ("updated_at", str(care.update_time)),
            ]) for care in user.care_set.all()
        ]
        return JsonResponse(result)


def friendlist(request):  #控糖团列表
    result = {'status': '1'}
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        result = OrderedDict([('status', '0')])
        result['list'] = [
            OrderedDict([
                ("id", flist.id),
                ("name", flist.bfriend.name),
                ("account", flist.bfriend.username),
                ("email", flist.bfriend.email),
                ("phone", flist.bfriend.phone),
                ("fb_id", flist.bfriend.phone),
                ("status", flist.bfriend.phone),
                ("group", flist.bfriend.group),
                ("birthday", flist.bfriend.birthday),
                ("height", flist.bfriend.height),
                ("gender", flist.bfriend.gender),
                ("verified", flist.bfriend.verified),
                ("privacy_policy", flist.bfriend.privacy_policy),
                ("must_change_password", flist.bfriend.must_change_password),
                ("badge", flist.bfriend.badge),
                ("group", flist.bfriend.group),
                ("group", flist.bfriend.group),
                ("relation_type", "1"),  #暂定1
            ]) for flist in user.answers_user.all()
        ]
        return JsonResponse(result)


def lastupload(request):  #最后更新时间
    result = {'status': '1'}
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        result = OrderedDict([('status', '0')])
        result['last_upload'] = OrderedDict([
            ("blood_pressure", user.userblood_set.last().update_time),
            ("weight", user.userweight_set.last().update_time),
            ("blood_sugar", user.userbloodsugar_set.last().update_time),
            ("diet", user.dietmod_set.last().update_time),
        ])
        return JsonResponse(result)


def notification(request):  #親友團通知
    result = '1'
    # try:
    if True:
        if request.method == 'POST':
            s = Session.objects.get(
                pk=request.POST.get('token', '')).get_decoded()  #解密
            user = Patient.objects.get(id=s['_auth_user_id'])  #决定user
            form = NotificationForm(json.loads(request.body.decode("utf-8")))
            if form.is_valid():
                message = form.cleaned_data['message']
                inotif = notificationmod.objects.create(message=message,
                                                        patient=user)
                inotif.save()
                result = '0'
    return JsonResponse({'status': result})


def friendsend(request):  #送出控糖團邀請(知道别人的邀请码后，向邀请码的主人送邀请)
    result = '1'
    if request.method == 'POST':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        form = receiveForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            fri = Patient.objects.get(
                invite_code=form.cleaned_data['invite_code'])
            # for aid in user.answers_user.all():
            #     if user.id == aid.afriend.id:
            #         result = '2'
            #         raise Exception("1")
            # for aid in user.relay_to_user.all():
            #     if user.id == aid.bfriend.id:
            #         result = '2'
            #         raise Exception("2")
            atype = form.cleaned_data['atype']
            aatype = receivemod.objects.create(atype=atype,
                                               areceive=user,
                                               breceive=fri)
            aatype.save()
            result = '0'
    return JsonResponse({'status': result})


def friendrequests(request):  #列出邀请列表
    result = {'status': '1'}
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        fri = user.breceive_user.all()
        result = OrderedDict([('status', '0')])
        result['requests'] = [
            OrderedDict([
                ("id", flist.id),
                ("user_id", user.id),
                ("relation_id", "1"),
                ("type", flist.atype),
                ("status", "0"),
                ("created_at", str(user.created_at)),
                ("updated_at", str(user.updated_at)),
                ("user",
                 OrderedDict([
                     ("id", flist.areceive.id),
                     ("name", flist.areceive.name),
                     ("account", flist.areceive.username),
                     ("email", flist.areceive.email),
                     ("phone", flist.areceive.phone),
                     ("fb_id", flist.areceive.phone),
                     ("status", flist.areceive.phone),
                     ("group", flist.areceive.group),
                     ("birthday", flist.areceive.birthday),
                     ("height", flist.areceive.height),
                     ("gender", flist.areceive.gender),
                     ("verified", flist.areceive.verified),
                     ("privacy_policy", flist.areceive.privacy_policy),
                     ("must_change_password",
                      flist.areceive.must_change_password),
                     ("badge", flist.areceive.badge),
                     ("created_at", str(flist.areceive.created_at)),
                     ("updated_at", str(flist.areceive.updated_at)),
                 ])),
            ]) for flist in user.breceive_user.all()
        ]
        return JsonResponse(result)


def friendaccept(request, idd):  #接受
    print("--------------------")
    result = {'status': '1'}
    if request.method == 'GET':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        r = receivemod.objects.get(id=idd)
        acuser = user
        bcuser = r.areceive
        print("--------------------")
        if user.id in [r.areceive.id, r.breceive.id]:
            r.accept_or_not = '1'  #是否接受邀请1是0否
            r.save()
            print(r.accept_or_not)
            print("--------------------")
            friendaa = friendmod.objects.create(afriend=acuser, bfriend=bcuser)
            friendaa.save()
            result = {'status': '0'}
    return JsonResponse(result)


def friendremove(request, idd):  #删除邀请表
    result = {'status': '1'}
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        r = receivemod.objects.get(id=idd)
        r.delete()
        result = {'status': '0'}
    return JsonResponse(result)


def friendrefuse(request, idd):  #拒绝
    print("--------------------")
    result = {'status': '1'}
    if request.method == 'GET':
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        r = receivemod.objects.get(id=idd)
        acuser = user
        bcuser = r.areceive
        print("--------------------")
        if user.id in [r.areceive.id, r.breceive.id]:
            r.accept_or_not = '0'  #是否接受邀请1是0否
            r.save()
            print(r.accept_or_not)
            print("--------------------")
            result = {'status': '0'}
    return JsonResponse(result)


def friendresults(request):  #控糖团结果
    result = {'status': '1'}
    if request.method == 'GET':
        result = {'status': '0'}
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')).get_decoded()
        user = Patient.objects.get(id=s['_auth_user_id'])
        fri = user.breceive_user.all()
        result = OrderedDict([('status', '0')])
        result['results'] = [
            OrderedDict([
                ("id", flist.id),
                ("user_id", user.id),
                ("relation_id", "1"),
                ("type", flist.atype),
                ("status", flist.accept_or_not),
                ("read", "true"),
                ("created_at", str(user.created_at)),
                ("updated_at", str(user.updated_at)),
                ("relation",
                 OrderedDict([
                     ("id", flist.areceive.id),
                     ("name", flist.areceive.name),
                     ("account", flist.areceive.username),
                     ("email", flist.areceive.email),
                     ("phone", flist.areceive.phone),
                     ("fb_id", flist.areceive.fb_id),
                     ("status", "Normal"),
                     ("group", flist.areceive.group),
                     ("birthday", flist.areceive.birthday),
                     ("height", flist.areceive.height),
                     ("gender", flist.areceive.gender),
                     ("unread_records", "[0,0,0]"),
                     ("verified", flist.areceive.verified),
                     ("privacy_policy", flist.areceive.privacy_policy),
                     ("must_change_password",
                      flist.areceive.must_change_password),
                     ("badge", flist.areceive.badge),
                     ("created_at", str(flist.areceive.created_at)),
                     ("updated_at", str(flist.areceive.updated_at)),
                 ])),
            ]) for flist in user.breceive_user.all()
        ]
        return JsonResponse(result)


def friendremove(request):  #移除好友
    result = {'status': '1'}
    s = Session.objects.get(
        pk=request.headers.get('Authorization', '')).get_decoded()
    user = Patient.objects.get(id=s['_auth_user_id'])
    if request.method == 'DELETE':
        data = json.loads(request.body.decode("utf-8"))
        if all(
            [user.answers_user.filter(id=ids).exists()
             for ids in data["ids"]]):
            [user.answers_user.get(id=ids).delete() for ids in data["ids"]]
            result = {'status': '0'}
    return JsonResponse(result)
