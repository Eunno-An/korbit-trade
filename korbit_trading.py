import json
import math
import pykorbit
import time
import requests
import base64
import hmac, hashlib
import urllib.parse

ORDER_BTC_AMOUNT = 0.002
TARGET_TRADE_VOLUME = 1000000000
TICKER = "btc"

with open('./secrets.json') as f:
    secrets = json.load(f)


secret_info = secrets['korbit']
api_key = secret_info['api_key']
secret = secret_info['secret']
email = secret_info['email']
password = secret_info['password']
korbit = pykorbit.Korbit(api_key, secret)
# korbit.buy_market_order(TICKER, 9800)
# korbit.sell_limit_order(TICKER, 45000, 0.28)

trade_krw = 0
print(korbit.get_balances()[TICKER])
initial_balance = korbit.get_balances()[TICKER]["available"]
initial_balance = math.floor(float(initial_balance) * 10000) / 10000
print(initial_balance) # remain_btc_amount
while True:
    if trade_krw > TARGET_TRADE_VOLUME:
        exit(0)
    print(initial_balance, ORDER_BTC_AMOUNT)
    if initial_balance <= ORDER_BTC_AMOUNT:
        orderbook_data = pykorbit.get_orderbook(TICKER)
        # {'timestamp': 1711263042883, 'bids': [['93045000', '0.00001091', '1'], ['93025000', '0.01220204', '1'], ['93024000', '0.07278064', '1'], ['93023000', '0.00377768', '1'], ['93022000', '0.00153748', '1'], ['93010000', '0.00107515', '1'], ['93000000', '0.06642193', '1'], ['92999000', '0.00010752', '1'], ['92996000', '0.0043926', '1'], ['92995000', '0.01005377', '1'], ['92994000', '0.02184809', '1'], ['92993000', '0.00106161', '1'], ['92992000', '0.01105682', '1'], ['92991000', '0.00170152', '1'], ['92990000', '0.03487229', '1'], ['92989000', '0.04518127', '1'], ['92988000', '0.0027961', '1'], ['92987000', '0.0013947', '1'], ['92985000', '0.00224136', '1'], ['92980000', '0.00123271', '1'], ['92974000', '0.00066231', '1'], ['92973000', '0.02151162', '1'], ['92964000', '0.00118328', '1'], ['92961000', '0.00028297', '1'], ['92959000', '0.00167199', '1'], ['92956000', '0.00013734', '1'], ['92955000', '0.00568489', '1'], ['92954000', '0.00011095', '1'], ['92950000', '0.0001538', '1'], ['92937000', '0.00059708', '1'], ['92930000', '0.00024662', '1'], ['92921000', '0.00008619', '1'], ['92916000', '0.03337276', '1'], ['92905000', '0.0001', '1'], ['92900000', '0.09990583', '1'], ['92899000', '0.00021528', '1'], ['92898000', '0.00005489', '1'], ['92896000', '0.0003', '1'], ['92890000', '0.00099972', '1'], ['92889000', '0.00006659', '1'], ['92880000', '0.0001', '1'], ['92873000', '0.00008015', '1'], ['92870000', '0.0001', '1'], ['92866000', '0.00107682', '1'], ['92862000', '0.0064612', '1'], ['92858000', '0.00010769', '1'], ['92850000', '0.0018237', '1'], ['92842000', '0.2999', '1'], ['92840000', '0.00247156', '1'], ['92837000', '0.00032781', '1']], 'asks': [['93056000', '0.00375387', '1'], ['93057000', '0.03012945', '1'], ['93079000', '0.1072', '1'], ['93205000', '0.01082795', '1'], ['93256000', '0.0001', '1'], ['93271000', '0.0001', '1'], ['93286000', '0.0001', '1'], ['93292000', '0.01292875', '1'], ['93301000', '0.0001', '1'], ['93316000', '0.0001', '1'], ['93330000', '0.00005536', '1'], ['93333000', '0.04075', '1'], ['93349000', '0.07271469', '1'], ['93400000', '0.02116261', '1'], ['93411000', '0.1433', '1'], ['93412000', '0.2258', '1'], ['93440000', '0.05351027', '1'], ['93472000', '0.00655559', '1'], ['93488000', '0.00120432', '1'], ['93490000', '0.2569689', '1'], ['93500000', '0.11604323', '1'], ['93527000', '0.00062376', '1'], ['93547000', '0.00086898', '1'], ['93549000', '0.00106895', '1'], ['93554000', '0.0023731', '1'], ['93561000', '0.00106882', '1'], ['93579000', '0.00106861', '1'], ['93582000', '0.00106858', '1'], ['93588000', '0.00106851', '1'], ['93590000', '0.00106849', '1'], ['93600000', '0.00194656', '1'], ['93631000', '0.00321042', '1'], ['93637000', '0.756', '1'], ['93653000', '0.00005339', '1'], ['93671000', '0.00604734', '1'], ['93700000', '0.00250698', '1'], ['93722000', '0.00008985', '1'], ['93800000', '0.00021321', '1'], ['93872000', '0.00106528', '1'], ['93873000', '0.00106526', '1'], ['93901000', '0.00106495', '1'], ['93918000', '0.00267318', '1'], ['93937000', '0.00230168', '1'], ['93942000', '0.0052', '1'], ['93952000', '0.00018737', '1'], ['93970000', '0.05', '1'], ['93999000', '0.00010744', '1'], ['94000000', '0.12645743', '1'], ['94009000', '0.00199677', '1'], ['94112000', '0.0004081', '1']]}
        
        bid_price = float(orderbook_data['bids'][0][0]) + 1000# 호가창에서 최대 매수 호가 가격보다 1000원 많이
        # print(bid_price)
        result = korbit.buy_limit_order(TICKER, bid_price, ORDER_BTC_AMOUNT - initial_balance)
        # print("result: ",result)
        outstanding_order_data = korbit.get_open_orders(TICKER, 0, 1)
        print("outstanding_order_data", outstanding_order_data)
        count = 0
        while outstanding_order_data != [] and outstanding_order_data != []:
            if count > 5 :
                print("지정가  매수 주문 미체결로 취소 뒤 재주문합니다.")
                count = 0
                print(outstanding_order_data)
                if outstanding_order_data != [] and outstanding_order_data != []:
                    id = int(outstanding_order_data[0]['id'])
                    if korbit.cancel_order(TICKER, id):
                        print(f"{id}취소 완료")
                    
                time.sleep(0.5)
                orderbook_data = pykorbit.get_orderbook(TICKER)
                bid_price = float(orderbook_data['bids'][0][0]) + 1000
                remain_btc_amount = korbit.get_balances()[TICKER]["available"]
                remain_btc_amount = math.floor(float(initial_balance) * 10000) / 10000
                print("remain_btc_amount", remain_btc_amount)
                if remain_btc_amount == ORDER_BTC_AMOUNT:
                    break
                else:
                    result = korbit.buy_limit_order(TICKER, bid_price, ORDER_BTC_AMOUNT - remain_btc_amount)
            count += 1
            outstanding_order_data = korbit.get_open_orders(TICKER, 0, 5)
        print("지정가 매수 주문 체결 확인")
        trade_krw += bid_price * ORDER_BTC_AMOUNT

    remain_btc_amount = korbit.get_balances()[TICKER]["available"]
    remain_btc_amount = math.floor(float(remain_btc_amount) * 10000) / 10000
    
    if remain_btc_amount > 0:
        orderbook_data = pykorbit.get_orderbook(TICKER)
        # print(orderbook_data)
        ask_price = float(orderbook_data['asks'][0][0])
        result = korbit.sell_limit_order(TICKER, ask_price, remain_btc_amount)
        print("매도 정보", ask_price, result)
        outstanding_order_data = korbit.get_open_orders(TICKER, 0, 1)
        print("outstanding_order_data", outstanding_order_data)
        count = 0
        while outstanding_order_data != [] and outstanding_order_data != []:
            if count > 5 :
                print("지정가 매도 주문 미체결로 취소 뒤 재주문합니다.")
                count = 0
                if outstanding_order_data != [] and outstanding_order_data != []:
                    id = int(outstanding_order_data[0]['id'])
                    if korbit.cancel_order(TICKER, id):
                        print(f"{id}취소 완료")
                time.sleep(0.5)
                orderbook_data = pykorbit.get_orderbook(TICKER)
                ask_price = float(orderbook_data['asks'][0][0]) 
                remain_btc_amount = korbit.get_balances()[TICKER]["available"]
                remain_btc_amount = math.floor(float(remain_btc_amount) * 10000) / 10000
                if remain_btc_amount == 0:
                    break
                else:
                    result = korbit.sell_limit_order(TICKER, ask_price, remain_btc_amount)
            count += 1
            outstanding_order_data = korbit.get_open_orders(TICKER, 0, 5)
        print("지정가 매도 주문 체결 확인")
        trade_krw += ask_price * ORDER_BTC_AMOUNT
    usePrice = float( korbit.get_balances()[TICKER]["available"]) * 10000 / 10000
    print( f"현재 사용금액: { initial_balance - usePrice }" )
    print(f"현재 거래량: {trade_krw}")
