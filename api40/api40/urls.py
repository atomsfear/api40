"""api40 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import diabetes.views as dv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('.well-known/acme-challenge/<str:token>', dv.acme),

    ###########登入###########
    path('api/register/', dv.register),  # 1.註冊
    path('api/auth/', dv.auth),  # 2.登入
    path('api/verification/send/', dv.send),  # 3.發送驗證碼
    path('api/verification/check/', dv.vcheck),  # 3.檢查驗證碼
    path('api/password/forgot/', dv.forgot),  # 4.忘記密碼
    path('api/password/reset/', dv.reset),  # 5.重設密碼
    path('api/user/privacy-policy/', dv.privacy_policy),  # 13.隱私權聲明 FBLogin
    path('api/register/check/', dv.rcheck),  # 38.註冊確認

    ##########個人資訊##########
    path('api/user/', dv.personal_info),  # 7.個人資訊設定，12.個人資訊
    path('api/user/default/', dv.default),  # 11.個人預設值
    path('api/user/setting/', dv.setting),  # 35.個人設定

    #########糖化血色素#########
    path('api/user/a1c/', dv.a1c),  # 32.糖化血色素，33.送糖化血色素，34.刪除糖化血色素

    ########就醫及藥物資訊########
    path('api/user/medical/', dv.medical),  # 30. 就醫資訊，31. 更新就醫資訊
    path('api/user/drug-used/', dv.drug_used),  # 41.藥物資訊，42.上傳藥物資訊，43.刪除藥物資訊

    ############單一############
    path('api/share/', dv.share),  # 23.分享
    path('api/share/<int:relation_type>/', dv.share),  # 24.查看分享（含自己分享出去的）
    path('api/news/', dv.news),  # 29. 最新消息
    path('api/user/badge/', dv.badge),  # 39.更新badge

    path('api/user/blood/pressure/', dv.ublood),  # 血压
    path('api/user/weight/', dv.uweight),  # 体重
    path('api/user/blood/sugar/', dv.ubloodsugar),  # 血糖
    path('api/user/diet/', dv.userdiet),  # 饮食日记
    path('api/user/diary/', dv.diary),  # 日记列表
    path('api/friend/code/', dv.friendcode),  # 控糖团邀请码
    path('api/user/records/', dv.userrecords),  # 上一笔资料
    path('api/user/care/', dv.usercare),  # 发送关怀资讯
    path('api/user/last-upload/', dv.lastupload),  # 最后更新时间
    path('api/notification/', dv.notification),  # 親友團通知
    path('api/friend/list/', dv.friendlist),  # 控糖团列表
    path('api/friend/send/', dv.friendsend),  # 送出控糖团邀请
    path('api/friend/requests/', dv.friendrequests),  # 获取控糖团邀请（列表）
    path('api/friend/<int:idd>/accept/', dv.friendaccept),  # 接受控糖团邀请
    path('api/friend/<int:idd>/remove/', dv.friendremove),  # 删除邀请
    path('api/friend/<int:idd>/refuse/', dv.friendrefuse),  # 拒绝控糖团邀请
    path('api/friend/results/', dv.friendresults),  # 控糖团结果
    path('api/friend/remove/', dv.friendremove),  # 删除好友

    # 以下網址結尾無斜線。

    ###########登入###########
    path('api/register', dv.register),  # 1.註冊
    path('api/auth', dv.auth),  # 2.登入
    path('api/verification/send', dv.send),  # 3.發送驗證碼
    path('api/verification/check', dv.vcheck),  # 3.檢查驗證碼
    path('api/password/forgot', dv.forgot),  # 4.忘記密碼
    path('api/password/reset', dv.reset),  # 5.重設密碼
    path('api/user/privacy-policy', dv.privacy_policy),  # 13.隱私權聲明 FBLogin
    path('api/register/check', dv.rcheck),  # 38.註冊確認

    ##########個人資訊##########
    path('api/user', dv.personal_info),  # 7.個人資訊設定，12.個人資訊
    path('api/user/default', dv.default),  # 11.個人預設值
    path('api/user/setting', dv.setting),  # 35.個人設定

    #########糖化血色素#########
    path('api/user/a1c', dv.a1c),  # 32.糖化血色素，33.送糖化血色素，34.刪除糖化血色素

    ########就醫及藥物資訊########
    path('api/user/medical', dv.medical),  # 30. 就醫資訊，31. 更新就醫資訊
    path('api/user/drug-used', dv.drug_used),  # 41.藥物資訊，42.上傳藥物資訊，43.刪除藥物資訊

    ############單一############
    path('api/share', dv.share),  # 23.分享
    path('api/share/<int:relation_type>', dv.share),  # 24.查看分享（含自己分享出去的）
    path('api/news', dv.news),  # 29. 最新消息
    path('api/user/badge', dv.badge),  # 39.更新badge
    ##########個人資訊##########
    path('api/user', dv.personal_info),  # 7.個人資訊設定，12.個人資訊
    path('api/user/default', dv.default),  # 11.個人預設值
    path('api/user/blood/pressure', dv.ublood),  # 血压
    path('api/user/weight', dv.uweight),  # 体重
    path('api/user/blood/sugar', dv.ubloodsugar),  # 血糖
    path('api/user/diet', dv.userdiet),  # 饮食日记
    path('api/user/diary', dv.diary),  # 日记列表
    path('api/friend/code', dv.friendcode),  # 控糖团邀请码
    path('api/user/records', dv.userrecords),  # 上一笔资料
    path('api/user/care', dv.usercare),  # 发送关怀资讯
    path('api/user/last-upload', dv.lastupload),  # 最后更新时间
    path('api/notification', dv.notification),  # 親友團通知
    path('api/friend/list', dv.friendlist),  # 控糖团列表
    path('api/friend/send', dv.friendsend),  # 送出控糖团邀请
    path('api/friend/requests', dv.friendrequests),  # 获取控糖团邀请（列表）
    path('api/friend/<int:idd>/accept', dv.friendaccept),  # 接受控糖团邀请
    path('api/friend/<int:idd>/remove', dv.friendremove),  # 删除邀请
    path('api/friend/<int:idd>/refuse', dv.friendrefuse),  # 拒绝控糖团邀请
    path('api/friend/results', dv.friendresults),  # 控糖团结果
    path('api/friend/remove', dv.friendremove),  # 删除好友
    # path('api/friend/<int:idd>/remove', dv.friendremove),  #拒绝控糖团邀请（只拒绝不删除）
]
