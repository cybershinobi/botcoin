import time
import datetime
import poloniex
import os, sys, getopt

k_key = 'your-key-from-poloniex'
k_secret = 'your-secret-from-poloniex'

help_msg = '-p --period\t\tthe period that the bot wait for'


class Model():
    def __init__(self,argv):
        self.conn = poloniex.Poloniex(k_key, k_secret)
        self.prices = []
        self.currency = 0
        self.update = 10
        self.period = 0
        self.starttime = 0
        self.endtime = 0
        self.perVal = [300,900,1800,7200,14400,86400]
        self.main(argv)

    def main(self,argv):   
        
        try:
            opts, args = getopt.getopt(argv,"hp:c:t:e:s:",["help","period=","currency=","starttime=","endtime=","strategy="])
        except getopt.GetoptError as err:
            print(str(err))
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-h','--help'):
                print(help_msg)
            elif opt in ('-p','--period'):
                if (int(arg) in self.perVal):
                    self.period = int(arg)
                else:
                    print('Not allowed period! Poloniex requires 300,900,1800,7200,14400,86400.')    
                    sys.exit(1)
            elif opt in ('-c','--currency'):
                self.currency = arg
            elif opt in ('-t','--starttime'):
                self.starttime  = arg
            elif opt in ('-e','--endtime'):
                self.endtime = arg    
            elif opt in ('-s','--strategy'):
                if (arg == 'chart'):
                    self.chartData()
                elif(arg == 'bot'):
                    self.bot()
                elif (arg == 'history'):
                    self.tradeHistory()                    
                else:
                    print('Chose a strategy. Type --help to see the suported strategies.')        


    def lastPrice(self):
        ticker = self.conn.returnTicker()
        last = ticker[self.currency]['last']
        print (last)

    def isOpen(self):
        orders = self.conn.returnOpenOrders(self.currency)
        print(orders)

    def tradeHistory(self):
        print(self.conn.marketTradeHist(self.currency,1405699200,1405749900)[:]) #teste

    def chartData(self):
        if (self.starttime):
            graph = self.conn.returnChartData(str(self.currency),self.period,self.starttime,self.endtime)
            getChart = graph.pop(0)
            returnedChart = getChart['weightedAverage']
        print(returnedChart)    

    def bot(self):
        #file = open('prices.txt', 'w')
        while True:
            try:
                currentPrice = self.conn.returnTicker()
                lastPrice = currentPrice[self.currency]['last']
                #self.prices.append(float(lastPrice))
                #file.write('{:%H:%M:%S},{}\n'.format(datetime.datetime.now(),lastPrice))
                print('{:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()) + ' ' + self.currency + ': '+str(lastPrice))
                #self.movingAvg = sum(self.prices) / len(self.prices)
                #file.flush()
                #os.fsync(file.fileno())

                time.sleep(int(self.update))
            except KeyboardInterrupt:
                print('\nUser interruption... Shutting down bot...')
                time.sleep(2)
                #file.close()
                break


if __name__ == '__main__':
    Model(sys.argv[1:])
    
