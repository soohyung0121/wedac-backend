import json
import bcrypt
import jwt
import re
import uuid
import requests
import random
import time

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text

from .models import User
from .token import account_activation_token
from .utils import make_signature, login_decorator
from .text import message
from my_settings import SECRET, EMAIL, SMS, APP_KEY, SECRET
from .models import User 

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

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User.objects.create(
                email    = data['email'],
                password = hashed_password,
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