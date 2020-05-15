from django.db import models

class BaseCurrency(models.Model):
    kor_name             = models.CharField(max_length = 10)
    code                 = models.CharField(max_length = 10)
    base_currency_image  = models.URLField(max_length = 2000)
    minimum_amount       = models.DecimalField(max_digits=20, decimal_places=4)
    fee                  = models.DecimalField(max_digits=5, decimal_places=2, null = True)

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
    quote_price    = models.DecimalField(max_digits = 20, decimal_places = 7)
    krw_price      = models.IntegerField()
    volume         = models.DecimalField(max_digits = 20, decimal_places = 10)
    date           = models.DateField()
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'closetime_currencies'

class CurrencyInfo(models.Model):
    code           = models.CharField(max_length = 50, null=True)
    title          = models.CharField(max_length = 50, null=True)
    category       = models.CharField(max_length = 50)
    volume         = models.CharField(max_length = 50)
    algorithm      = models.CharField(max_length = 100)
    foundation     = models.CharField(max_length = 200)
    company        = models.CharField(max_length = 30)
    website        = models.CharField(max_length = 30)
    representative = models.CharField(max_length = 100)
    feature        = models.CharField(max_length = 1000)

    class Meta:
        db_table = 'currency_infos'

class CurrencyChart(models.Model):
    date           = models.DateField()
    open_price     = models.DecimalField(max_digits=10, decimal_places=1)
    high_price     = models.DecimalField(max_digits=10, decimal_places=1)
    low_price      = models.DecimalField(max_digits=10, decimal_places=1)
    close_price    = models.DecimalField(max_digits=10, decimal_places=1)
    base_volume    = models.DecimalField(max_digits = 20, decimal_places = 2)
    quote_volume   = models.DecimalField(max_digits = 20, decimal_places = 2)
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'currency_charts'

class CoinSummary(models.Model):
    base_currency      = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null=True)
    quote_currency     = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null=True)
    present_price      = models.DecimalField(max_digits=20, decimal_places=8)
    sub_krw_price      = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    close_price        = models.DecimalField(max_digits=20, decimal_places=8)
    change_rate        = models.DecimalField(max_digits=4, decimal_places=2)
    change_price       = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    high_price         = models.DecimalField(max_digits=20, decimal_places=8)
    low_price          = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_volume = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    transaction_price  = models.DecimalField(max_digits=20, decimal_places=8, null=True)

    class Meta:
        db_table = 'coin_summaries'

class OrderUnit(models.Model):
    base_currency  = models.ForeignKey('BaseCurrency', on_delete = models.SET_NULL, null = True)
    quote_currency = models.ForeignKey('QuoteCurrency', on_delete = models.SET_NULL, null = True)
    unit           = models.DecimalField(max_digits = 20, decimal_places = 7)

    class Meta:
        db_table = 'order_units'


