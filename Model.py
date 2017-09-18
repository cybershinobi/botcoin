import time
import datetime
from poloniex import Poloniex
import os



class Model():
    def __init__(self, period, currency, key, secret):
        self.period = period
        self.conn = Poloniex(key, secret)
        self.currency = currency
        self.prices = []
        self.movingAvg = 0

    def lastPrice(self):
        ticker = self.conn.returnTicker()
        last = ticker[self.currency]['last']
        print (last)

    def isOpen(self):
        orders = self.conn.returnOpenOrders(self.currency)
        print(orders)

    def tradeHistory(self):
        print(self.conn.returnMarketTradeHistory(self.currency)[0])

    def toChart(self):
        file = open('prices.txt', 'w')
        while True:
            try:
                currentPrice = self.conn.returnTicker()
                lastPrice = currentPrice[self.currency]['last']
                self.prices.append(float(lastPrice))
                file.write('{:%H:%M:%S},{}\n'.format(datetime.datetime.now(),lastPrice))
                #print('{:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()) + ' Currency Pair: ' + self.currency + ' Price: '+str(lastPrice)+' Moving Average: '+str(self.movingAvg))
                #self.movingAvg = sum(self.prices) / len(self.prices)
                file.flush()
                os.fsync(file.fileno())

                time.sleep(self.period)
            except KeyboardInterrupt:
                file.close()
                break


if __name__ == '__main__':
    I = Model(10,'BTC_XMR','your-key-here','your-secret-here')
    I.toChart()
