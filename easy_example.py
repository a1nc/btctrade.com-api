# -*- coding:utf-8 -*-

import requests
import json
import time
import hashlib
import hmac

# 输入btctrade.com申请的API公钥、密钥
public_key = 'xxxxx-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx'
secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def get_trade_info(coin_type):
    try:
        url = 'https://api.btctrade.com/api/ticker?coin=%s' % str(coin_type)
        response = requests.get(url,timeout=2).text
        js_dict = json.loads(response)
        return js_dict
    except Exception as e:
        print(e)
        return False
        # high: 最高价
        # low: 最低价
        # buy: 买一价
        # sell: 卖一价
        # last: 最新成交价
        # vol: 成交量(最近的24小时)
        # time: 返回数据时服务器时间


def get_trade_record(coin_type):
    try:
        url = 'https://api.btctrade.com/api/trades?coin=%s' % str(coin_type)
        response = requests.get(url,timeout=2).text
        js_dict = json.loads(response)
        return js_dict
    except Exception as e:
        print(e)
        return False
        # date: 成交时间
        # price: 交易价格
        # amount: 交易数量
        # tid: 交易ID
        # type: 交易类型


def generate_signature(params):
    _md5key = hashlib.md5(secret_key.encode('utf-8')).hexdigest()
    _md5key = str(_md5key).encode('utf-8')
    url = 'https://api.btctrade.com/api/balance/'
    # get the ms of time
    _params = {}
    _params['key'] = public_key
    _params['nonce'] = str(time.time()).split('.')[0]
    _params['version'] = '2'
    for key in params:
        _params[key]=params[key]
    _str = ''
    for key in _params:
        _str += key+'='+_params[key]+'&'
    _str = _str[0:-1]
    _hmac = hmac.new(_md5key,msg=_str.encode('utf-8'),digestmod='sha256')
    sign_key = _hmac.hexdigest()
    _params['signature'] = sign_key
    resoponse = requests.post(url,data=_params)
    print(resoponse.text)


post_params = {}
generate_signature(post_params)
