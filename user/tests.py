import jwt
import json
import unittest

from django.test import TestCase, Client
from user.models import User
from unittest.mock import patch, MagicMock

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

if __name__ == '__main__':
    unittest.main()

