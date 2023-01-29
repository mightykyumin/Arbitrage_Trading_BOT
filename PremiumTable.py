import sys
import time
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation
import binanceTrading
import UpbitTrading

tickers =['BTC','ETH','XLM','DOT','XRP','TRX','ADA','NEO','QTUM','EOS','IOTA','GAS','BTT','WAXP','QKC','SC','STEEM','HIVE','ICX']

class OrderbookWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.alive = True


    def run(self):
        data = {}
        while self.alive:
            for ticker in tickers:
                ub = UpbitTrading.get_current_price_in_BTC(ticker)

                bn = binanceTrading.get_current_price(ticker)
                pr = binanceTrading.calculate_premium(ticker)
                data[ticker] =[ub,bn,pr]

                self.dataSent.emit(data)
                time.sleep(0.1)



    def close(self):
        self.alive = False
class OrderbookWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("premiumTable.ui", self)

        self.ow = OrderbookWorker()
        self.ow.dataSent.connect(self.updateData)
        self.ow.start()


    def updateData(self, data):

        try:
            # display binance currencies price
            i =0
            for ticker, price in data.items():

                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(ticker)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(format(price[0],'.8f'))))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(price[1]))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(price[2]))
                i =i+1
        except:
            pass


    def closeEvent(self, event):
        self.ow.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ow = OrderbookWidget()
    ow.show()
    exit(app.exec_())