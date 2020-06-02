import json
import bcrypt
import jwt
import re
import uuid
import unittest
import random

from .models import User
from .utils  import login_decorator
from wedac.settings import SECRET_KEY
from unittest.mock import patch, MagicMock

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.test import TestCase, Client

class KakaoLoginTest(unittest.TestCase):
    def setup(self):
        User.objects.create(
                platform_id='1234567890',
                name='yeni',
                email='yeni@gg.com'
                )

    def teardown(self):
        User.objects.get(platform_id='1234567890').delete()

    @patch('user.views.requests')
    def test_kakao_login_success(self, mocked_request):
        c = Client()

        class FakeResponse:
            def json(self):
                return {
                        "id" : 1234567890,
                        "properties" : {"nickname" : "yeni"},
                        "kakao_account" : {"email": "yeni@gg.com"}
                        }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        response = c.post('/user/kakao-login',**{"HTTP_AUTHORIZATION" : "fake_token.1234", "content_type" :"applications/json"})
        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_kakao_login_fail(self, mocked_request):
        c = Client()

        class FakeResponse:
            def json(self):
                return {
                        "d" : 1234567890,
                        "properties" : {"nickname" : "yeni"},
                        "kakao_account" : {"email": "yeni@gg.com"}
                        }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        response = c.post('/user/kakao-login',**{"HTTP_AUTHORIZATION" : "fake_token.1234", "content_type" :"applications/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email = 'soohyung0121@gmail.com',
            password = '12345Aa!!'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        client = Client()
        User = {
            'email' : 'soo123@gmail.com',
            'password' : '12345Aa!',
            'check_password' : '12345Aa!'
        }
        response = client.post('/user/sign-up', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signup_userexists(self):
        client = Client()
        User = {
            'email' : 'soohyung0121@gmail.com',
            'password' : '12345Aa!',
            'check_password' : '12345Aa!'
        }
        response = client.post('/user/sign-up', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'USER_ALREADY_EXISTS'})

    def test_signup_emailerror(self):
        client = Client()
        User = {
            'email' : 'soohyung0121gmail.com',
            'password' : '12345Aa!',
            'check_password': '12345Aa!'
        }
        response = client.post('/user/sign-up', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EMAIL_VALIDATION_ERROR'})

    def test_signup_keyerror(self):
        client = Client()
        User = {
            'id' : 'soohyu@gmail.com',
            'password' : '12345Aa!',
            'check_password': '12345Aa!'
        }
        response = client.post('/user/sign-up', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEYS'})

    def test_check_password(self):
        client = Client()
        User = {
            'email' : 'soohg0121@gmail.com',
            'password' : '12345Aa!',
            'check_password' : '12345aA!'
        }
        response = client.post('/user/sign-up', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'PASSWORD_INCONSISTENCE'})

class SignInTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('12345aA!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User(
            email = 'soohyung0121@gmail.com',
            password = hashed_password
        ).save()

    def tearDown(self):
        User.objects.all().delete()

    def test_signin(self):
        client = Client()
        User = {
            'email' : 'soohyung0121@gmail.com',
            'password' : '12345aA!'
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        access_token = jwt.encode({'email': User['email']}, SECRET_KEY, algorithm='HS256').decode('utf-8')
        self.assertEqual(response.json(), {'access_token' : access_token})

    def test_invalid_email(self):
        client = Client()
        User = {
            'email' : 'soo0121@gmail.com',
            'password' : '12345aA!'
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_signin_keyerror(self):
        client = Client()
        User = {
            'id': 'soohyung0121@gmail.com',
            'password': '12345aA!'
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_invalid_password(self):
        client = Client()
        User = {
            'email': 'soohyung0121@gmail.com',
            'password': '345Aa',
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()

