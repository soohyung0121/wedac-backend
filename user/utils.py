import hashlib
import hmac
import base64
import jwt
from django.http import JsonResponse
from user.models import User
from wedac.settings import SECRET_KEY

def make_signature(timestamp):
    access_key = 'OzIojdvP4wtP50c8NTJb'
    secret_key = 'r4gRgGMr2CYKIs9JqHHrdE5XoH5ZCtBJOTUoqTQ6'
    secret_key = bytes(secret_key, 'UTF-8')
    uri = '/sms/v2/services/ncp:sms:kr:259220815670:wedac/messages'
    message = "POST " + uri + "\n" + timestamp + "\n"+ access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod = hashlib.sha256).digest()).decode('UTF-8')
    return signingKey

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if "Authorization" not in request.headers:
            return JsonResponse({'error_code' : "INVALID_LOGIN"}, status = 401)
        encode_token = request.headers['Authorization']
        try:
            data = jwt.decode(encode_token.encode('utf-8'), SECRET_KEY, algorithms = 'HS256')
            user = User.objects.get(email = data['email'])
            request.user = user
        except jwt.DecodeError:
            return JsonResponse({'error_code' : 'UNKNOWN_USER'}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({'error_code' : 'INVALID_USER'}, status = 401)
        return func(self, request, *args, **kwargs)
    return wrapper
