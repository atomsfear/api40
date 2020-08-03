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
]
