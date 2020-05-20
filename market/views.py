import json
from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import BaseCurrency, QuoteCurrency, RealtimeCurrency, CoinSummary, ClosetimeCurrency
from user.models import User, Order, UserWallet

class CoinDetail(View):
    def get(self, request, quote_code, base_code):
        try:
            quote = QuoteCurrency.objects.get(code=quote_code)
            base = BaseCurrency.objects.get(code=base_code)

            if quote is None and base is None:
                return JsonResponse({'message' : 'SELECT CURRENCY PAIR'}, status=400)

            coin = CoinSummary.objects.get(base_currency=base.id, quote_currency=quote.id)
            data = { 
                    'market'                : base.code,
                    'coin'                  : quote.code,
                    'coin_kor_name'         : QuoteCurrency.objects.get(id=quote.id).kor_name,
                    'thumbnail_url'         : quote.quote_currency_image,
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
        
        except KeyError:
            JsonResponse({'message' : 'DO NOT EXIST'}, status = 500)

class CoinList(View):
    def get(self, request, base_code):
        try:
            base_id = BaseCurrency.objects.get(code=base_code).id
            coins = CoinSummary.objects.filter(base_currency_id=base_id)
            summary = []
            for coin in coins:
                quote_id  = coin.quote_currency_id
                quote = QuoteCurrency.objects.get(id=quote_id)
                base = BaseCurrency.objects.get(id=base_id)
                data={}
                data = {
                        'coin_code'         : quote.code,
                        'coin_kor_name'     : quote.kor_name,
                        'thumbnamil_url'    : quote.quote_currency_image,
                        'present_price'     : coin.present_price,
                        'sub_krw_price'     : coin.sub_krw_price,
                        'change_rate'       : coin.change_rate,
                        'transaction_price' : coin.transaction_price
                }
                summary.append(data)
            return JsonResponse({ 'market_code' : base.code,
                                'market_kor_name' : base.kor_name,
                                'history': summary}, status = 200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

class CoinHistory(View):
    def get(self, request, quote_code, base_code):
        try:
            quote = QuoteCurrency.objects.get(code=quote_code)
            base = BaseCurrency.objects.get(code=base_code)
            coin_history = ClosetimeCurrency.objects.filter(base_currency=base.id, quote_currency=quote.id)
            coin_name = quote.code
            history = []
            for coin in coin_history:
                data = {}
                data = {                
                        'date'          : coin.date,
                        'close_price'   : coin.quote_price,
                        'krw_price'     : coin.krw_price,
                        'volume'        : coin.volume
                }
                history.append(data)
            return JsonResponse({ 
                                'market'        : base.code,
                                'coin'          : quote.code,
                                'coin_kor_name' : quote.kor_name,
                                'daily_history'       : history}, status = 200)
        
        except KeyError:
            JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

