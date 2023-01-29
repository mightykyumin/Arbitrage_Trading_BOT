import pyupbit
import time
import datetime
# Method : Long-Term Secrets to Short -Term Trading

# 1. 가격 변동폭 계산 : 투자하려는 가상회폐의 전일 고가에서 전일 저가를 빼서 가상화폐의 가격 변동폭을 구합니다
# 2. 매수 기준 : 당일 시간에서 (변동폭 *0.5) 이상 상승하면 매수
# 3. 매도 기준 : 당일 종가에 매도합니다.

# API key 값 가져오기
with open("upbitkey.txt") as f:
    lines = f.readlines()

con_key = lines[0].strip()
sec_key = lines[1].strip()

# upbit 클래스 객체를 생성하는데 초기화자로 키값을 전달합니다.
upbit = pyupbit.Upbit(con_key, sec_key)

def get_current_price(ticker):
    try:
        data = pyupbit.get_orderbook("KRW-"+ticker, 10)
        price = data[0]['orderbook_units'][0]['ask_price']
        return price
    except:
        return None
def get_current_price_in_BTC(ticker):
    try:
        data = pyupbit.get_orderbook("KRW-" + ticker, 1)
        price = data[0]['orderbook_units'][0]['ask_price']

        data2 = pyupbit.get_orderbook("KRW-BTC", 1)
        btc_price = data2[0]['orderbook_units'][0]['ask_price']
        ticker_btc = price/btc_price
        return ticker_btc
    except:
        return None
upbit.get_balance("KRW")

