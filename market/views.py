import json
from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import BaseCurrency, QuoteCurrency, RealtimeCurrency, CoinSummary, ClosetimeCurrency, OrderUnit 
from user.models import User, Order, UserWallet
from user.utils import login_decorator
from django.core.exceptions import ObjectDoesNotExist


class CoinDetail(View):
    def get(self, request, quote_code, base_code):
        try:
            if CoinSummary.objects.select_related('base_currency', 'quote_currency').get(base_currency__code=base_code, quote_currency__code=quote_code):
                coin = CoinSummary.objects.select_related('base_currency', 'quote_currency').get(base_currency__code=base_code, quote_currency__code=quote_code)
                data = {
                        'market'                : coin.base_currency.code,
                        'coin'                  : coin.quote_currency.code,
                        'coin_kor_name'         : coin.quote_currency.kor_name,
                        'thumbnail_url'         : coin.quote_currency.quote_currency_image,
                        'present'               : coin.present_price,
                        'sub_krw'               : coin.sub_krw_price,
                        'low'                   : coin.low_price,
                        'high'                  : coin.high_price,
                        'change_price'          : coin.change_price,
                        'change_rate'           : coin.change_rate,
                        'volume_24hours'        : coin.transaction_volume,
                        'price_24hour'          : coin.transaction_price,
                        }
                return JsonResponse({'coin_detail':[data]}, status = 200)
            return JsonResponse({'message': "QUERY NOT EXIST"}, status=400)
        except CoinSummary.DoesNotExist:
            return JsonResponse({'message' : "CURRENCY DOES NOT EXIST"}, status =400)


class CoinList(View):
    def get(self, request, base_code):
        try:
            coins = CoinSummary.objects.select_related('base_currency', 'quote_currency').filter(base_currency__code=base_code)
            summary = [{
                'coin_code'         : coin.quote_currency.code,
                'coin_kor_name'     : coin.quote_currency.kor_name,
                'thumbnamil_url'    : coin.quote_currency.quote_currency_image,
                'present_price'     : coin.present_price,
                'high_price'        : coin.high_price,
                'low_price'         : coin.low_price,
                'sub_krw_price'     : coin.sub_krw_price,
                'change_rate'       : coin.change_rate,
                'transaction_price' : coin.transaction_price
            } for coin in coins]
            if coins.first() == None:
                return JsonResponse({'message' : "CURRENCY DOES NOT EXIST"}, status =400)
            base = coins.first()
            return JsonResponse({ 'market_code' : base.base_currency.code,
                                'market_kor_name' : base.base_currency.kor_name,
                                'history': summary}, status = 200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)


class CoinHistory(View):
    def get(self, request, quote_code, base_code):
        try:
            coin_history = ClosetimeCurrency.objects.select_related('base_currency', 'quote_currency').filter(base_currency__code=base_code, quote_currency__code=quote_code)
            history = [{
                    'date'          : coin.date,
                    'close_price'   : coin.quote_price,
                    'krw_price'     : coin.krw_price,
                    'volume'        : coin.volume
            } for coin in coin_history]
            if coin_history.first() is None:
                return JsonResponse({'message' : "CURRENCY DOES NOT EXIST"}, status =400)

            return JsonResponse({
                'market'        : item.base_currency.code,
                'coin'          : item.quote_currency.code,
                'coin_kor_name' : item.quote_currency.kor_name,
                'daily_history' : history}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
        except ClosetimeCurrency.DoesNotExist:
            return JsonResponse({'message' : "CURRENCY DOES NOT EXIST"}, status =400)


class CoinRealtime(View):
    def get(self, request, quote_code, base_code):
        try:
            coin_realtime = RealtimeCurrency.objects.select_related('base_currency', 'quote_currency').filter(base_currency__code=base_code, quote_currency__code=quote_code)
            standard = CoinSummary.objects.select_related('base_currency', 'quote_currency').get(base_currency__code=base_code, quote_currency__code=quote_code).close_price

            sobs = [ coin.order_type for coin in coin_realtime ]
            price = [ coin.price for coin in coin_realtime ] 
            rate = [ round((coin.price-standard)/standard, 2) for coin in coin_realtime ]
            volume = [ coin.volume for coin in coin_realtime ]
            item = coin_realtime.first()
            return JsonResponse({
                        'market' : item.base_currency.code,
                        'coin'   : item.quote_currency.code,
                        'realtime' : {'sob':sobs, 'price':price, 'rate':rate, 'volume':volume}}, status=200)
        except KeyError:
            JsonResponse({'message' : 'INVALID_KEY'}, status=400)

class CoinOrderUnit(View):
    def get(self, request, quote_code, base_code):
        try:
            unit = OrderUnit.objects.select_related('base_currency', 'quote_currency').get(base_currency__code='KRW', quote_currency__code='BTC')
            order_units = {
                'market' : unit.base_currency.code,
                'coin'   : unit.quote_currency.code,
                'unit'   : unit.unit
                }
            return JsonResponse({'order_unit':order_units}, status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

class CoinInfoView(View):
    def get(self, request, quote_currency):
        try:
            currency_info = CurrencyInfo.objects.get(code = quote_currency)
            data = [{
                'code'           : currency_info.code,
                'title'          : currency_info.title,
                'category'       : currency_info.category,
                'volume'         : currency_info.volume,
                'algorithm'      : currency_info.algorithm,
                'foundation'     : currency_info.foundation,
                'company'        : currency_info.company,
                'website'        : currency_info.website,
                'representative' : currency_info.representative,
                'feature'        : currency_info.feature
            }]
            return JsonResponse({'message' : data}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)

class CoinChartView(View):
    def get(self, request, quote_currency, base_currency):
        try:
            coin_charts = CurrencyChart.objects.select_related('base_currency', 'quote_currency').filter(base_currency__code = base_currency, quote_currency__code = quote_currency)
            data = [{
                'quote_currency' : coin_chart.quote_currency.code,
                'base_currency'  : coin_chart.base_currency.code,
                'date'           : coin_chart.date,
                'open_price'     : coin_chart.open_price,
                'high_price'     : coin_chart.high_price,
                'low_price'      : coin_chart.low_price,
            } for coin_chart in coin_charts]
            return JsonResponse({'message' : data}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)
