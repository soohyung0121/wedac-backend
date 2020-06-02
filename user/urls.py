from django.urls import path
from .views import KakaoLogin, SignInView, SignUpView
from .views import Activate, SmsSend, SmsValidaton, BankAccount
from .views import OrderView, UpdateWallet


urlpatterns = [
        path('/sign-up', SignUpView.as_view()),
        path('/activate/<str:uidb64>/<str:token>', Activate.as_view()),
        path('/sign-in', SignInView.as_view()),
        path('/sms', SmsSend.as_view()),
        path('/sms/check', SmsValidaton.as_view()),
        path('/bankaccount', BankAccount.as_view()),

        path('/kakao-login', KakaoLogin.as_view()),
        path('/deposit', UpdateWallet.as_view()),
        path('/deposit/check', UpdateWallet.as_view()),
        path('/<str:base_code>/<str:quote_code>/order', OrderView.as_view())
]
