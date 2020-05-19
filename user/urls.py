from django.urls import path
from .views import KakaoLogin 

urlpatterns = [
        path('/kakao-login', KakaoLogin.as_view()),
]
