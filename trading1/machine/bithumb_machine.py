import requests
import time
import math
from trading1.machine.base_machine import Machine
import configparser
import json
import base64
import hashlib
import urllib
import hmac


class BithumbMachine(Machine):
    """
    빗썸 거래소와의 거래를 위한 클래스.
    BASE_API_URL은 REST API 호출을 위한 기본 URL 입니다.
    TRADE_CURRENCY_TYPE은 빗썸에서 거래가 가능한 화폐의 종류입니다
    """
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM", "BTG", "EOS"]

    def __init__(self):
        """BithumbMachine 클래스에서 가장 먼저 호출되는 메서드.
        config.ini 파일에서 connect_key, secret_key, username을 읽어옴"""
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect_key']
        self.CLIENT_SECRET = config['BITHUMB']['secret_key']
        self.USER_NAME = config['BITHUMB']['username']

    def get_ticker(self, currency_type=None):
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        ticker_api_path = "/public/ticker/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path)
        response_json = res.json()
        result = dict()
        result["timestamp"] = str(response_json['data']["date"])
        result["last"] = response_json['data']["closing_price"]
        result["bid"] = response_json['data']["buy_price"]
        result["ask"] = response_json['data']["sell_price"]
        result["high"] = response_json['data']["max_price"]
        result["low"] = response_json['data']["min_price"]
        result["volume"] = response_json['data']["volume_1day"]
        return result

    def get_filled_orders(self, currency_type=None):
        """ 체결 정보를 가져올 수 있는 메서드입니다.
        Note: 가장 최근 100개만 받을 수 있습니다.
        Args: currency_type(str) - 화폐 종류를 입력받으며, 종류는 TRADE_CURRENCY_TYPE에 정의돼 있습니다
        Returns: 최근 체결 정보를 딕셔너리의 리스트 형태로 반환합니다.
        """
        if currency_type is None:
            raise Exception("Need to currency type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        params = {'offset': 0, 'count': 100}
        orders_api_path = "/public/recent_transactions/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path, params=params)
        result = res.json()
        return result

    def microtime(self, get_as_float=False): # static으로 바꾸면 아래서 self를 통한 접근이 불가능해짐
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self):
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2]  # str type elements. [:2]는 없어도 원하는 결과 나옴
        return mt_array[1] + mt_array[0][2:5]  # 역시 str이라 가능한 부분

    def get_nonce(self):
        return self.usecTime()  # str(int(time.time()))

    def get_signature(self, encoded_payload, secret_key):
        """
        Args: encoded_payload(str)-인코딩된 페이로드 값, secret_key-서명할 때 사용할 사용자의 secret_key
        Returns: 사용자의 secret_key로 서명된 데이터 반환
        """
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)
        api_sign = base64.b64encode(signature.hexdigest().encode('utf-8'))
        return api_sign

    def get_wallet_status(self, currency_type=None):
        """사용자의 지갑 정보 조회
        화폐 종류를 입력받은 뒤 사용자의 지갑에 화폐별 잔액을 딕셔너리 형태로 반환.
        """
        if currency_type is None:
            raise Exception("Need to currency type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        wallet_status_api_path = "/info/balance"
        endpoint = "/info/balance"
        url_path = self.BASE_API_URL + wallet_status_api_path

        endpoint_item_array = {
            "endpoint" : endpoint,
            "currency" : currency_type
        }

        uri_array = dict(endpoint_item_array)  # concatenate the two arrays.. 진짜로 왜 이렇게 하는지 모르겠음
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.usecTime()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key':self.CLIENT_ID,
                   'Api-Sign':self.get_signature(utf8_data,bytes(utf8_key)),
                   'Api-Nonce':nonce
                   }

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result["data"]

    def get_list_my_orders(self, currency_type=None):
        """사용자의 지갑 정보 조회
        화폐 종류를 입력받은 뒤 사용자의 지갑에 화폐별 잔액을 딕셔너리 형태로 반환.
        """
        if currency_type is None:
            raise Exception("Need to currency type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        wallet_status_api_path = "/info/orders"
        endpoint = "/info/orders"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint" : endpoint,
            "currency" : currency_type
        }

        uri_array = dict(endpoint_item_array)  # concatenate the two arrays.. 진짜로 왜 이렇게 하는지 모르겠음
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + stvirtur_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')
        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key':self.CLIENT_ID,
                   'Api-Sign':self.get_signature(utf8_data,bytes(utf8_key)),
                   'Api-Nonce':nonce
                   }

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result["data"]

    def get_token(self):
        pass

    def set_token(self):
        pass

    def get_username(self):
        return self.USER_NAME

    def buy_order(self):
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        endpoint = "/trade/place"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint": endpoint,
            "order_currency": currency_type,
            "payment_currenct": "KRW",
            "units": qty,
            "price": price,
            "type": "bid"
        }

        uri_array = dict(endpoint_item_array)  # Concatenate the two arrays.
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result


    def sell_order(self):
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        endpoint = "/trade/place"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint": endpoint,
            "order_currency": currency_type,
            "payment_currenct": "KRW",
            "units": qty,
            "price": price,
            "type": "ask"
        }

        uri_array = dict(endpoint_item_array)  # Concatenate the two arrays.
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result

    def cancel_order(self):
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        endpoint = "/trade/cancel"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint": endpoint,
            "currency": currency_type,
            "type": order_type,
            "order_id": order_id
        }

        uri_array = dict(endpoint_item_array)  # Concatenate the two arrays.
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result

    def get_my_order_status(self, currency_type=None, order_id=None):
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        endpoint = "/info/order_detail"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint": endpoint,
            "currency": currency_type
        }

        uri_array = dict(endpoint_item_array)  # Concatenate the two arrays.
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result["data"]

    def __repr__(self):
        return "(Bithumb %s)" % self.USER_NAME

    def __str__(self):
        return str("Bithumb")
