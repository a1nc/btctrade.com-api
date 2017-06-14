# -*- coding:utf-8 -*-
import requests
import json
import time
import hashlib
import hmac

# 输入btctrade.com申请的API公钥、密钥
public_key = 'xxxxx-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx'
secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

timeout_value = 2


def api_trade_info(coin_type):
    try:
        url = 'https://api.btctrade.com/api/ticker?coin=%s' % str(coin_type)
        response = requests.get(url, timeout=timeout_value).text
        js_dict = json.loads(response)
        return js_dict
    except Exception as e:
        print('ERROR_API_TRADE_INFO: ', e)
        return False
        # json example:
        # {"high":0,"low":0,"buy":1850,"sell":1851.1,"last":1851.1,"vol":10000,"time":1420711226}
        # high: 最高价
        # low: 最低价
        # buy: 买一价
        # sell: 卖一价
        # last: 最新成交价
        # vol: 成交量(最近的24小时)
        # time: 返回数据时服务器时间


def api_trade_record(coin_type):
    try:
        url = 'https://api.btctrade.com/api/trades?coin=%s' % str(coin_type)
        response = requests.get(url, timeout=timeout_value).text
        js_dict = json.loads(response)
        return js_dict
    except Exception as e:
        print('ERROR_API_TRADE_RECORD:  ', e)
        return False
        # json example:
        # [{"date":"1420713686","price":1773.1,"amount":0.656,"tid":"5236256","type":"buy"}]
        # date: 成交时间
        # price: 交易价格
        # amount: 交易数量
        # tid: 交易ID
        # type: 交易类型


def generate_data(params):
    md5key = hashlib.md5(secret_key.encode('utf-8')).hexdigest()
    md5key = str(md5key).encode('utf-8')
    dict = {}
    dict['key'] = public_key
    dict['nonce'] = str(time.time()).split('.')[0]
    dict['version'] = '2'
    for key in params:
        dict[key] = params[key]
    string = ''
    for key in dict:
        string += key + '=' + dict[key] + '&'
    string = string[0:-1]
    hmac_encode = hmac.new(md5key, msg=string.encode('utf-8'), digestmod='sha256')
    dict['signature'] = hmac_encode.hexdigest()
    return dict


def api_get_info():
    # get the user information
    url = 'https://api.btctrade.com/api/balance/'
    try:
        response = requests.post(url, data=generate_data({}), timeout=timeout_value)
        # print(response.text)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_GET_INFO:  ', e)
        return False
        # json example
        # {"uid":123,"nameauth":0,"moflag":"0","asset":"1861.36","btc_balance":0,"btc_reserved":0,"
        # ltc_balance":0,"ltc_reserved":0, "doge_balance":0,"doge_reserved":0,"ybc_balance":0,"ybc_
        # reserved":0,"cny_balance":0,"cny_reserved":0}
        # uid: 用户id
        # nameauth: 是否实名认证
        # 1
        # 实名, 0
        # 未实名
        # moflag: 是否绑定手机
        # 1
        # 绑定, 0
        # 未绑
        # asset: 折合资产
        # *_balance: 币种余额
        # *_reserved: 币种冻结


def api_market_trades(coin_type):
    url = 'https://api.btctrade.com/api/trades?coin=%s' % str(coin_type)
    try:
        response = requests.post(url, data=generate_data({}), timeout=timeout_value)
        # print(response.text)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_MARKET_TRADES:  ', e)
        return False
        # [{"date":"1420713686","price":1773.1,"amount":0.656,"tid":"5236256","type":"buy"}]
        # date: 成交时间
        # price: 交易价格
        # amount: 交易数量
        # tid: 交易ID
        # type: 交易类型


def api_get_orders(coin_type, order_type, sort_type):
    # coin: 交易币种（btc, eth, ltc, doge, ybc）
    # type: 挂单类型[open:正在挂单, all:所有挂单]
    # since: 时间戳, 查询某个时间戳之后的挂单
    # ob: 排序, ASC, DESC
    url = 'https://api.btctrade.com/api/orders/'
    dict = {}
    dict['coin'] = str(coin_type)
    dict['type'] = str(order_type)
    dict['ob'] = str(sort_type)
    try:
        response = requests.post(url, data=generate_data(dict))
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_GET_ORDERS:  ', e)
        return False
        # id: 挂单ID
        # datetime: 挂单时间
        # type: 类型（buy, sell）
        # price: 挂单价格
        # status: 状态：open(开放), closed(全部成交), cancelled(撤消)
        # amount_original: 挂单数量
        # amount_outstanding: 剩余数量


def api_get_fetch_order(order_id):
    url = 'https://api.btctrade.com/api/fetch_order/'
    # id: 挂单ID
    dict = {}
    dict['id'] = str(order_id)
    try:
        response = requests.post(url, data=generate_data(dict), timeout=timeout_value)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_GET_FETCH_ORDER:  ', e)
        return False
        # id: 挂单ID
        # datetime: 挂单时间
        # type: 类型（buy, sell）
        # price: 挂单价格
        # amount_original: 挂单数量
        # amount_outstanding: 剩余数量
        # status: 状态：open(开放), closed(结束), cancelled(撤消)
        # sum_number: 成交总数量
        # sum_money: 成交额
        # avg_price: 成交均价


# ##############完整权限方法列表############ #
def api_cancel_order(order_id):
    url = 'https://api.btctrade.com/api/cancel_order/'
    # id: 挂单ID
    dict = {}
    dict['id'] = str(order_id)
    try:
        response = requests.post(url, data=generate_data(dict), timeout=timeout_value)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_CANCEL_ORDER:  ', e)
        return False
        # {"result":true,"message":"success"}


def api_buy_order(coin_type, amount, price):
    url = 'https://api.btctrade.com/api/buy/'
    dict = {}
    dict['coin'] = str(coin_type)
    dict['amount'] = str(amount)
    dict['price'] = str(price)
    try:
        response = requests.post(url, data=generate_data(dict), timeout=timeout_value)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_BUY_ORDER:  ', e)
        return False
        # key: 公钥
        # signature: 签名
        # nonce: 自增数
        # coin: 交易币种（btc, eth, ltc, doge, ybc）
        # amount: 购买数量
        # price: 购买价格



def api_sell_order(coin_type, amount, price):
    url = 'https://api.btctrade.com/api/sell/'
    dict = {}
    dict['coin'] = str(coin_type)
    dict['amount'] = str(amount)
    dict['price'] = str(price)
    try:
        response = requests.post(url, data=generate_data(dict), timeout=timeout_value)
        return json.loads(response.text)
    except Exception as e:
        print('ERROR_API_SELL_ORDER:  ', e)
        return False
        # key: 公钥
        # signature: 签名
        # nonce: 自增数
        # coin: 交易币种（btc, eth, ltc, doge, ybc）
        # amount: 购买数量
        # price: 购买价格

# test 
print(api_trade_info('doge'))
print('------------------------')
print(api_trade_record('doge'))
print('------------------------')
print(api_market_trades('doge'))
print('------------------------')
print(api_get_info())
print('------------------------')
print(api_get_fetch_order('361844821'))
print('------------------------')
data = api_sell_order('doge', '100', '1')
id = data['id']
time.sleep(1.5)
print('------------------------')
print(api_buy_order('doge', '100', '0.001'))
time.sleep(1.5)
print('------------------------')
print(api_cancel_order(id))
print('------------------------')
