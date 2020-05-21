from django.urls import path
from .views import KakaoLogin, SignUpView, SignInView, Activate

urlpatterns = [
        path('/kakao-login', KakaoLogin.as_view()),
        path('/sign-up', SignUpView.as_view()),
        path('/activate/<str:uidb64>/<str:token>', Activate.as_view()),
        path('/sign-in', SignInView.as_view())
]
