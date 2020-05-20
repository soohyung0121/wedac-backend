from django.urls import path
from .views import CoinDetail, CoinList, CoinHistory

urlpatterns = [
        path('/<str:base_code>/<str:quote_code>', CoinDetail.as_view()),
        path('/<str:base_code>', CoinList.as_view()),
        path('/<str:base_code>/<str:quote_code>/history', CoinHistory.as_view()),
        ]

