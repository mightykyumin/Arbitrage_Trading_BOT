import sys
from binance.client import Client
from PyQt5.QtCore import QTime, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit
import datetime
import binanceTrading
import UpbitTrading

# Connect with upbit and binance


tickers = ['ETH', 'XLM', 'DOT', 'XRP', 'TRX', 'ADA', 'NEO', 'QTUM', 'EOS', 'IOTA', 'GAS', 'BTT', 'WAXP', 'QKC', 'SC',
           'STEEM', 'HIVE', 'ICX']
CheapTransmission = ['NEO', 'EOS', 'TRX', 'IOST', 'GAS', 'XRP', 'WAVES', 'XLM','ZIL','ARK','LSK','XTZ','HIVE','META']


class TradingWorker(QThread):
    tradingSent = pyqtSignal(str, dict)

    def __init__(self, upbit, binance):
        super().__init__()
        self.alive = True
        self.upbit = upbit
        self.binance = binance

    def run(self):
        PremiumList = {}
        PremiumSenderList = {}
        while self.alive:
            # calculate the Premium and check with the greatest premium
            for ticker in tickers:
                # gets Premium percentage
                PremiumList[ticker] = binanceTrading.calculate_premium_price(CheapTransmission)
            # find the max ticker which has highest premium
            krw = self.upbit.get_balance("KRW")


            # BinanceBalance = self.binance.get_balance("BTC")
            # Upbit buying
            if (int(krw) > 5000):
                # calculate the Premium and check with the greatest premium


                max_ticker = max(PremiumList, key=PremiumList.get)
                # If there is a ticker with great premium purchase

                if(PremiumList[max_ticker]>0.8):

                    min_ticker = min(PremiumList, key=PremiumList.get)
                    # Purchase smallest premium coin and send it to Binance

                    # Calculate the amount of coin to purchase
                    unit = krw / float(PremiumSenderList[min_ticker][1]) *0.9995 #Take out the fee
                    try:
                        #purchase coin
                        order = self.upbit.buy_limit_order('KRW-'+str(min_ticker), PremiumSenderList[min_ticker][1], unit)
                        #Send coin to Binance
                        self.Upbit_to_Binance(min_ticker)
                        self.tradingSent.emit("BUY", order)
                    except:
                        self.tradingSent.emit("Purchase Fail", {})
            # If there is coin in Binance not in Upbit
            else:
                tradingTicker =''
                balance = self.binance.fetch_balance()
                for ticker in CheapTransmission:
                    # change coin into BTC
                    if(balance[ticker]>10):
                        orderbook = self.binance.get_order_book(symbol=ticker + 'BTC')

                        current_price = orderbook['asks'][0][0]
                        self.binance.order_limit_sell(
                            symbol = ticker+'BTC',
                            quantity = balance[ticker],
                            price = current_price
                        )
                #purchase the most premium coin
                max_ticker = max(PremiumList, key=PremiumList.get)
                orderbook = self.binance.get_order_book(symbol=ticker+'BTC')
                current_price = orderbook['asks'][0][0]
                self.binance.order_limit_buy(
                    symbol = max_ticker + 'BTC',
                    quantity = balance['BTC'],
                    price = current_price
                )







    def Upbit_to_Binance(self, ticker):
        for sender in CheapTransmission:
            pass

    def Binnace_to_Upbit(self, ticker):
        pass

    def close(self):
        self.alive = False


# Bring UI
form_class = uic.loadUiType("main.ui")[0]


# Open MainWindow UI
class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Arbitrage Trading Bot")
        self.upbit = None
        self.binance = None

        # Button Setup
        self.upbitButton.clicked.connect(self.upbitBtnClicked)
        self.binanceButton.clicked.connect(self.binanceBtnClicked)
        self.StartButton.clicked.connect(self.startBtnClicked)

    # Login to Upbit account
    def upbitBtnClicked(self):
        apiKey = self.apikey1.text()
        secKey = self.seckey1.text()
        if len(apiKey) != 40 or len(secKey) != 40:
            self.textEdit.append("Key is not correct")
            return
        else:
            try:
                self.upbit = pyupbit.Upbit(apiKey, secKey)
            except:
                self.textEdit.append("Not correct Key")
                return
            self.textEdit.append("Upbit Login success")

    # Login to Binance account
    def binanceBtnClicked(self):
        apiKey = self.apikey2.text()
        secKey = self.seckey2.text()
        if len(apiKey) != 32 or len(secKey) != 32:
            self.textEdit.append("Key is not correct")
            return
        else:
            try:
                self.binance = Client(api_key=apiKey, api_secret=secKey)
            except:
                self.textEdit.append("Not correct Key")
                return
            self.textEdit.append("Binance Login success")

    # Start Trading
    def startBtnClicked(self):
        if (self.StartButton.text() == "StartTrading"):

            self.StartButton.setText("StopTrading")
            self.textEdit.append("-----------Start Trading------------")
            if (self.upbit != None):

                self.textEdit.append("Upbit current Balance :" + str(self.upbit.get_balance("KRW")))
            if (self.binance != None):
                self.textEdit.append("binance current Balance :" + str(self.upbit.get_balance("BTC")))

            self.Tb = TradingWorker(self.upbit, self.binance)
            self.Tb.tradingSent.connect(self.receiveTradingSignal)
            self.Tb.start()

        else:
            self.Tb.close()
            self.textEdit.append("---------End------------")
            self.StartButton.setText("StartTrading")

    def receiveTradingSignal(self, type, order_data):
        self.textEdit.append("Type :" + str(type))
        uuid = order_data['uuid']
        market = order_data['market']
        date = order_data['created_at']
        price = order_data['price']
        volume = order_data['volume']

        self.textEdit.append('Uuid = '+ str(uuid))
        self.textEdit.append('Market = ' + str(market))
        self.textEdit.append('Date = ' + str(date))
        self.textEdit.append('Price = ' + str(price))
        self.textEdit.append('Volume = ' + str(volume))
    def claseEvent(self, event):
        self.Tb.close()
        self.widget.closeEvent(event)
        self.widget_2.closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())
