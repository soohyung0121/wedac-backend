import json
from django.test import TestCase, Client
from .models import BaseCurrency, QuoteCurrency, CoinSummary, ClosetimeCurrency, CurrencyInfo

class CoinDetailTest(TestCase):
    def setUp(self):
        currency_info1 = CurrencyInfo.objects.create(
                id=20,
                code='AERGO',
                title='아르고(AERGO)',
                category='상호운용성 솔루션',
                volume='500,000,000 AERGO',
                algorithm='N/A',
                foundation='N/A',
                company='AERGO',
                website='https://www.aergo.io/',
                representative='Phil Zamani',
                feature='아르고는 한국의 블록체인 솔루션 기업 블로코가 기술 파트너로 참여하는 프로젝트로 엔터프라이즈 분야의 블록체인 플랫폼을 지향합니다.'
                )
        quote_currency1 =QuoteCurrency.objects.create(
                id=1,
                kor_name='아르고',
                code='AERGO',
                quote_currency_image='http://naver.me/I5jkoaGg',
                currency_info= currency_info1
                )
        base_currency1 = BaseCurrency.objects.create(
                id=1,
                kor_name='원화',
                code='KRW',
                base_currency_image='http://naver.mo/GdWA6DyY',
                minimum_amount=500.0000,
                fee=0.04
                )
        CoinSummary.objects.create(
                id=1,
                base_currency =base_currency1,
                quote_currency =quote_currency1,
                present_price=24.33000000,
                close_price=24.33000000,
                change_rate=0.00,
                change_price=0.00000,
                high_price=24.33000000,
                low_price=24.33000000,
                sub_krw_price=0.0000,
                transaction_price=0E-8,
                transaction_volume=0E-8
                )

    def tearDown(self):
        CurrencyInfo.objects.all().delete()
        QuoteCurrency.objects.all().delete()
        BaseCurrency.objects.all().delete()
        CoinSummary.objects.all().delete()

    def test_coin_detail_success(self):
        c = Client()
        response = c.get('/market/KRW/AERGO')
        self.assertEqual(response.json(), {
            "coin_detail": [
            {
            "market": "KRW",
            "coin": "AERGO",
            "coin_kor_name": "아르고",
            "thumbnail_url": "http://naver.me/I5jkoaGg",
            "present": "24.33000000",
            "sub_krw": "0.0000",
            "low": "24.33000000",
            "high": "24.33000000",
            "change_price": "0.00000",
            "change_rate": "0.00",
            "volume_24hours": "0E-8",
            "price_24hour": "0E-8"
                                }
                            ]
            })
        self.assertEqual(response.status_code, 200)

class CoinListTest(TestCase):
    def setUp(self):
        currency_info1 = CurrencyInfo.objects.create(
                id=1,
                code='ATOM',
                title='코스모스아톰(ATOM)',
                category='상호운용성 솔루션',
                volume='약 2.4억 ATOM',
                algorithm='Tendermint',
                foundation='Interchain Foundation',
                company='All In Bits',
                website='https://cosmos.network/',
                representative='Jae kwon',
                feature='PBFT를 개선한 텐더민트(Tendermint) 합의 알고리즘을 이용하여 블록체인간 전송의 확정성(Finality)을 수 초내에 가능케 했다는 점과, ATOM 토큰을 기반으로하는 강력한 거버넌스가 특징입니다.'
                )
        quote_currency2 =QuoteCurrency.objects.create(
                id=2,
                kor_name='코스모스아톰',
                code='ATOM',
                quote_currency_image='http://naver.me/Fn6fvdZJ',
                currency_info= currency_info1
                )
        base_currency2 = BaseCurrency.objects.create(
                id=2,
                kor_name='비트코인',
                code='BTC',
                base_currency_image='http://naver.me/xuMoeXYe',
                minimum_amount=0.0001,
                fee=0.04
                )
        CoinSummary.objects.create(
                id=2,
                base_currency =base_currency2,
                quote_currency =quote_currency2,
                present_price=0.00028100,
                close_price=0.00028100,
                change_rate=0.00,
                change_price=0.00000,
                high_price=0.00028100,
                low_price=0.00028100,
                sub_krw_price=3321.0000,
                transaction_price=0.00000000,
                transaction_volume=0.00000000
                )

    def tearDown(self):
        CurrencyInfo.objects.all().delete()
        QuoteCurrency.objects.all().delete()
        BaseCurrency.objects.all().delete()
        CoinSummary.objects.all().delete()

    def test_coin_list_success(self):
        c = Client()
        response = c.get('/market/BTC')
        self.assertEqual(response.json(), {
                    "market_code": "BTC",
                    "market_kor_name": "비트코인",
                    "history": [
                            {
                                "coin_code": "ATOM",
                                "coin_kor_name": "코스모스아톰",
                                "thumbnamil_url": "http://naver.me/Fn6fvdZJ",
                                "present_price": "0.00028100",
                                "sub_krw_price": "3321.0000",
                                "change_rate": "0.00",
                                "transaction_price": "0E-8"
                                    }
                                ]
                            })
        self.assertEqual(response.status_code, 200)

class CoinHistoryTest(TestCase):
    def setUp(self):
        currency_info33 = CurrencyInfo.objects.create(
                id=33,
                code='KLAY',
                title='코스모스아톰(ATOM)',
                category='플랫폼',
                volume='10,000,000,000KLAY',
                algorithm='BFT (Byzantine Fault Tolerance)',
                foundation='N/A',
                company='Ground X',
                website='https://www.klaytn.com/',
                representative='한재선',
                feature='카카오의 글로벌 퍼블릭 블록체인 프로젝트 Klaytn은 사용자 친화적인 블록체인 경험을 수백만에 제공하는 엔터프라이즈급 서비스 중심 플랫폼입니다. 효율적인 ‘하이브리드’ 설계를 통해 퍼블릭 블록체인과 프라이빗 블록체인의 기능을 결합하였으며, 엔터프라이즈급 안정성을 목표로 하는 고도로 최적화된 BFT기반 퍼블릭 블록체인입니다.'
                )
        quote_currency20 =QuoteCurrency.objects.create(
                id=20,
                kor_name='클레이',
                code='KLAY',
                quote_currency_image='http://naver.me/xasGCAqM',
                currency_info= currency_info33
                )
        base_currency1 = BaseCurrency.objects.create(
                id=1,
                kor_name='원화',
                code='KRW',
                base_currency_image='http://naver.mo/GdWA6DyY',
                minimum_amount=500.0000,
                fee=0.04
                )

    def tearDown(self):
        CurrencyInfo.objects.all().delete()
        QuoteCurrency.objects.all().delete()
        BaseCurrency.objects.all().delete()

    def test_coin_list_success(self):
        c = Client()
        response = c.get('/market/KRW/KLAY/history')
        self.assertEqual(response.json(), {
                "market": "KRW",
                "coin": "KLAY",
                "coin_kor_name": "클레이",
                "daily_history": []
            })
        self.assertEqual(response.status_code, 200)