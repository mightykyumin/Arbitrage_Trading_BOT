import pyupbit
import binanceTrading

client = binance.Client()
data = pyupbit.get_orderbook("KRW-"+'XLM', 10)
price = data[0]['orderbook_units'][0]['ask_price']
print(price)





