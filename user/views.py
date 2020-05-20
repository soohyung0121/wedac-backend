import json
import requests
import jwt

from django.http import JsonResponse, HttpResponse
from django.views import View

from my_settings import APP_KEY, SECRET
from .models import User, UserDeposit, UserWallet
from .utils import login_decorator


@login_decorator
class UpdateWallet(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)
            krw_balance = UserWallet.objects.get(user_id=user.id, asset_id=34, market_id=1)
            update_krw = data['price']
            side = data['deposit_side']
            if user.bank_account is not None:
                if side  == 0:
                    update_krw = -update_krw

                UserDeposit(
                        user         = user.id, 
                        deposit_side = side,
                        price        = update_krw
                        ).save()
                krw_balance.volume += update_krw
                return HttpResponse(status=200)
            return JsonResponse({'message':'DOES NOT HAVE BANK ACCOUNT'}, status=400)
        except KeyError:
            JsonResponse({'message': 'PERMISSION DENIED'}, status=401)


class KakaoLogin(View):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', None)
            url = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                    'Authorization' : f'Bearer {access_token}',
                    'Content-type'  : 'application/x-www-form-urlencoded; charset=utf-8'
            }
            response = requests.get(url, headers = headers)
            response = response.json()
        
            if User.objects.filter(platform_id = response['id']).exists():
                user = User.objects.get(platform_id= response['id'])
                jwt_token = jwt.encode({'id': user.id}, SECRET['secret'], algorithm='HS256').decode('utf-8')
                return JsonResponse({'token': jwt_token }, status = 200)
        
            user = User.objects.create(
                    platform_id = response['id'],
                    name        = response['properties']['nickname'],
                    email       = response['kakao_account'].get('email', None)
            )
            user_token = jwt.encode({'id':user.id}, SECRET['secret'], algorithm='HS256').decode('utf-8')
            return JsonResponse({'token': user_token }, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
    
