from django.db import models
from market.models import BaseCurrency, QuoteCurrency

class User(models.Model):
    uid           = models.CharField(max_length = 20)
    email         = models.CharField(max_length = 50)
    kakao_email   = models.CharField(max_length = 50)
    password      = models.CharField(max_length = 200)
    name          = models.CharField(max_length = 20, null=True)
    phone_number  = models.CharField(max_length = 30)
    bank_account  = models.CharField(max_length = 45, null =  True)
    bank_name     = models.CharField(max_length = 20)
    krw_balance   = models.IntegerField(null = True)

    class Meta:
        db_table = 'users'

class UserAccessLog(models.Model):
    ip_address     = models.CharField(max_length = 50)
    access_time    = models.DateTimeField(auto_now = True)
    access_os      = models.CharField(max_length = 20)
    access_browser = models.CharField(max_length = 50)
    user           = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'user_access_logs'

class UserDeposit(models.Model):
    deposit_side = models.CharField(max_length = 1)
    price        = models.IntegerField()
    user         = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'user_deposits'

class Order(models.Model):
    order_type  = models.CharField(max_length = 1)
    price       = models.IntegerField()
    quantity    = models.DecimalField(max_digits = 20, decimal_places = 10)
    order_dtime = models.DateTimeField(auto_now = True)
    user        = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    base_currency  = models.ForeignKey(BaseCurrency, on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey(QuoteCurrency, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'orders'

class Trade(models.Model):
    trade_dtime = models.DateTimeField(auto_now = True)
    fee_rate    = models.DecimalField(max_digits = 5, decimal_places = 2)
    order       = models.ForeignKey('Order', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'trades'

class UserWallet(models.Model):
    volume         = models.DecimalField(max_digits = 20, decimal_places = 10)
    krw_price      = models.IntegerField()
    user           = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey(QuoteCurrency, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'userwallets'