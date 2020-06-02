import json
import bcrypt
import requests
import jwt
import re
import uuid
import random
import time 

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.db.models import Sum

from .models import User, UserDeposit, UserWallet
from .token import account_activation_token
from .utils import make_signature, login_decorator
from .text import message
from market.models import BaseCurrency, QuoteCurrency 
from user.models import Order 
from my_settings import APP_KEY, SECRET, EMAIL, SMS


class SignUpView(View):
    VALIDATION_RULES = {
        'password' : lambda password : True if re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()<>?]){8,50}', password) else False,
    }
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : "USER_ALREADY_EXISTS"}, status = 400)

            for validation_name, validate in self.VALIDATION_RULES.items():
                if not validate(data[validation_name]):
                    return JsonResponse({'message' : 'EMAIL_INVALID_ERROR'}, status = 400)

            if data['password'] != data['check_password']:
                return JsonResponse({'message' : 'PASSWORD_INCONSISTENCE'}, status = 400)
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(
                email    = data['email'],
                password = hashed_password.decode('utf-8'),
                is_active= False
            )
            current_site = get_current_site(request)
            domain       = current_site.domain
            uidb64       = urlsafe_base64_encode(force_bytes(user.pk))
            token        = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)
            mail_title = "이메일 인증 요청"
            mail_to    = data['email']
            email      = EmailMessage(mail_title, message_data, to = [mail_to])
            email.send()
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)
        except ValidationError:
            return JsonResponse({'message' : 'EMAIL_VALIDATION_ERROR'}, status = 400)


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])
            return JsonResponse({'message' : 'AUTH FAIL'}, status = 400)
        except ValidationError:
            return JsonResponse({'message' : 'TYPE_ERROR'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'email' : user.email}, SECRET['secret'], algorithm = 'HS256').decode('utf-8')
                    return JsonResponse({'access_token' : access_token}, status = 200)
                return HttpResponse(status = 401)
            return HttpResponse(status = 401)
        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status = 400)


class SmsSend(View):
    timestamp = str(int(time.time() * 1000))
    def send_sms(self, phone_number, auth_number):
        headers = {
            'Content-Type'            : "application/json; charset=UTF-8",
            'x-ncp-apigw-timestamp'   : self.timestamp,
            'x-ncp-iam-access-key'    : SMS['ACCESS_KEY'],
            'x-ncp-apigw-signature-v2': make_signature(self.timestamp)
        }
        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": SMS['SEND_NUMBER'],
            "content": auth_number,
            "messages": [{"to": f"{phone_number}"}]
        }
        body = json.dumps(body)
        requests.post(SMS['API_URI'], headers = headers , data = body)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            input_phone_number = data['phone_number']
            created_auth_number = random.randint(1000,10000)
            self.send_sms(phone_number = input_phone_number, auth_number = created_auth_number)
            User.objects.filter(email = request.user.email).update(
                phone_number = input_phone_number,
                auth_number = created_auth_number
            )
            return HttpResponse(status = 200)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)


class SmsValidaton(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(email = request.user.email)
        try:
            if user.auth_number == int(data['auth_number']):
                return JsonResponse({'message' : data['auth_number']}, status = 200)
            return JsonResponse({'message' : data['auth_number']}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'error_code' : 'INVALID_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)


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


class BankAccount(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            uids = str(uuid.uuid5(uuid.NAMESPACE_DNS, data['name']))
            User.objects.filter(email = request.user.email).update(
                uid          = uids[:8],
                name         = data['name'],
                bank_account = data['bank_account'],
                bank_name    = data['bank_name']
            )

            UserWallet(
                    user_id=request.user.id,
                    asset_id=34,
                    market_id=1,
                    volume=0,
                    price=0
            ).save()

            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)

class UpdateWallet(View):
    @login_decorator 
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            krw_wallet = UserWallet.objects.get_or_create(
                    user_id=user.id, 
                    asset_id=34, 
                    market_id=1)

            deposit = int(data['price'])
            side = int(data['deposit_side'])

            if user.bank_account:
                if side == 0:
                    deposit = -deposit

                if krw_wallet[0].volume + deposit < 0:
                    return JsonResponse({'message': 'DEFFECIENT MONEY'}, status=400)

                UserDeposit(
                        user_id      = user.id, 
                        deposit_side = side,
                        price        = deposit
                        ).save()

                krw_wallet[0].volume += deposit
                krw_wallet[0].save()
                return JsonResponse({'message' : 'DEPOSIT UPDATED'}, status=200)
            return JsonResponse({'message':'USER HAVE NO BANK ACCOUNT'}, status=400)
        except KeyError:
                JsonResponse({'message': 'INVALID KEY'}, status=401)
                
    @login_decorator
    def get(self, request):
        try:
            user = request.user
            wallet = UserWallet.objects.select_related('market', 'asset').filter(user_id=user.id)
            user_wallet = [{
                'coin_name'   : coin.asset.code,
                'market_name' : coin.market.code,
                'volume'      : coin.volume,
                'price'       : coin.price
                } for coin in wallet]
            return JsonResponse({'my_wallet' : user_wallet}, status=200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

class OrderView(View):
    @login_decorator
    def post(self, request, base_code, quote_code):
        try:
            data = json.loads(request.body)
            user = request.user
            request_volume = float(data['volume'])
            request_price = float((data['price'].replace(',','')))
            total_price = request_price * request_volume
            
            base_id = BaseCurrency.objects.get(code=base_code).id
            quote_id = QuoteCurrency.objects.get(code=quote_code).id
            base_quote = QuoteCurrency.objects.get(code=base_code).id 

            wallet = UserWallet.objects.get_or_create(user_id=user.id, asset_id=quote_id, market_id=base_id)[0]
            coin = UserWallet.objects.get_or_create(user_id=user.id, asset_id=base_quote, market_id=base_id)[0]


            if total_price <= coin.volume:
                Order.objects.create(
                        base_currency_id  = wallet.market.id,
                        quote_currency_id = wallet.asset.id,
                        user_id        = user.id,
                        order_type     = int(data['order_type']),
                        price          = request_price,
                        quantity       = request_volume
                        )
                print('hi')
                if data['order_type']== '0':
                    request_volume *= -1
                wallet.volume = float(wallet.volume) + total_price
                wallet.save()
                return JsonResponse({"message":"ORDER REGISTERED"}, status = 200)
            return JsonResponse({"message":"NOT ENOUGH MONEY"})
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
