from django.db import models

class BaseCurrency(models.Model):
    kor_name             = models.CharField(max_length = 10)
    code                 = models.CharField(max_length = 10)
    base_currency_image  = models.URLField(max_length = 2000)
    minimum_amount       = models.IntegerField()

    class Meta:
        db_table = 'base_currencies'

class QuoteCurrency(models.Model):
    kor_name             = models.CharField(max_length = 30)
    code                 = models.CharField(max_length = 10)
    quote_currency_image = models.URLField(max_length = 2000)
    currency_info        = models.OneToOneField('CurrencyInfo', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'quote_currencies'

class RealtimeCurrency(models.Model):
    order_type     = models.CharField(max_length = 1)
    price          = models.IntegerField()
    volume         = models.DecimalField(max_digits = 20, decimal_places = 10)
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'realtime_currencies'

class ClosetimeCurrency(models.Model):
    close_price    = models.IntegerField()
    volume         = models.DecimalField(max_digits = 20, decimal_places = 10)
    date           = models.DateField(auto_now = True)
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'closetime_currencies'

class CurrencyInfo(models.Model):
    category       = models.CharField(max_length = 50)
    volume         = models.CharField(max_length = 50)
    algorithm      = models.CharField(max_length = 100)
    foundation     = models.CharField(max_length = 30)
    company        = models.CharField(max_length = 30)
    website        = models.CharField(max_length = 30)
    representative = models.CharField(max_length = 100)
    feature        = models.CharField(max_length = 1000)

    class Meta:
        db_table = 'currency_infos'

class CurrencyChart(models.Model):
    open_price     = models.IntegerField()
    high_price     = models.IntegerField()
    low_price      = models.IntegerField()
    close_price    = models.IntegerField()
    base_volume    = models.DecimalField(max_digits = 20, decimal_places = 10)
    quote_volume   = models.DecimalField(max_digits = 20, decimal_places = 10)
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'currency_charts'