import signal
import sys
import time
import threading
import ConfigParser
import bitstamp
import trademanager

class trader (threading.Thread):
    def __init__(self, threadID, name, app, profit):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
        self.app = app
        self.pollInterval = 2
        self.mode = "buying" #buying=buying bitcoins. selling=selling bitcoins for dollars.
        self.actedPrice = 0 # What were the price thread last buyed or sold.
        self.previousPrice = 0 # Previous polled price.
        self.previousBid = 0
        self.previousAsk = 0
        self.profit = profit
    
    def run(self):
        self.running = True
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        waited = 0
        holdHigh = 0
        while self.running == True:
            # Polling price information from
            currentPrice = self.app.currentPrice
            highPrice = self.app.highPrice
            lowPrice = self.app.lowPrice
            volume = self.app.volume
            bidPrice = float(self.app.bidPrice)
            askPrice = float(self.app.askPrice)
            
            #We want to record peak price of the time
            if bidPrice > holdHigh:
                holdHigh = bidPrice
            
            # Checking if we yet have price data.
            if currentPrice > -1:
                #print "Nonce for my next api call is: " + str(self.app.getNonce())
                
                decission = trademanager.TradeManager()
                exchange = self.app.api
                
                if self.mode == "buying":
                    if self.actedPrice == 0:
                        if exchange.balanceCheckUSD(self.app.getNonce(), cfg.tradeAmount, askPrice):
                            # Thread have not yet done single trade, buying first ins.
                            purchase = exchange.buyBitcoins(self.app.getNonce(), cfg.tradeAmount, askPrice)
                            if purchase["id"] > 0:
                                self.actedPrice = askPrice
                                self.mode = "selling"
                                purchase = None
                                holdHigh = 0
                                print "Bought first coins"
                        else:
                            print "Out of dollars"
                    else:
                        react = decission.decideBuy(currentPrice, highPrice, lowPrice, volume, bidPrice, askPrice, self.actedPrice, self.previousAsk)
                        if react.action == "buy":
                            if exchange.balanceCheckUSD(self.app.getNonce(), cfg.tradeAmount, askPrice):
                                purchase = exchange.buyBitcoins(self.app.getNonce(), cfg.tradeAmount, react.price)
                                if purchase["id"] > 0:
                                    self.actedPrice = float(react.price)
                                    self.mode = "selling"
                                    purchase = None
                                    holdHigh = 0
                                    print "Decided to buy bitcoins"
                                waited = 0
                            else:
                                print "Out of dollars"
                                waited += 1
                        elif waited > 160:
                            if exchange.balanceCheckUSD(self.app.getNonce(), cfg.tradeAmount, askPrice):
                                purchase = exchange.buyBitcoins(self.app.getNonce(), cfg.tradeAmount, askPrice)
                                if purchase["id"] > 0:
                                    self.actedPrice = askPrice
                                    self.mode = "selling"
                                    purchase = None
                                    holdHigh = 0
                                    print "Buyed bitcoins"
                                waited = 0
                        else:
                            waited += 1
                
                # We are on Selling mode
                else:
                    react = decission.decideSell(currentPrice, highPrice, lowPrice, volume, bidPrice, askPrice, self.actedPrice, self.previousBid, self.profit, holdHigh)
                    if react.action == "sell":
                        # TODO: Check if we have bitcoins (balance)
                        print "Selling bitcoins"
                        purchase = exchange.sellBitcoins(self.app.getNonce(), 0.1, react.price)
                        if purchase["id"] > 0:
                            self.actedPrice = float(react.price)
                            self.mode = "buying"
                            purchase = None
                            holdHigh = 0
                            print "Sold bitcoins"
    
            else:
                print "Price not available."
            time.sleep(self.pollInterval)
            self.previousPrice = currentPrice
            self.previousBid = bidPrice
            self.previousAsk = askPrice
        print "Exiting " + self.name

    def stop(self):
        self.running = False

class monitor (threading.Thread):
    def __init__(self, threadID, name, app):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
        self.pollInterval = 7
        self.app = app
    
    def run(self):
        self.running = True
        print "Starting " + self.name
        while self.running == True:
            #Get the last price for trading.
            try:
                pricedata = self.app.api.pullPrice()
                self.app.currentPrice = pricedata['last']
                self.app.highPrice = pricedata['high']
                self.app.lowPrice = pricedata['low']
                self.app.volume = pricedata['volume']
                self.app.bidPrice = pricedata['bid']
                self.app.askPrice = pricedata['ask']
                #print "Price " + str(self.app.currentPrice)
            except:
                print "Error on fetching price data"
                pass
            
            time.sleep(self.pollInterval)
        print "Exiting " + self.name

    def stop(self):
        self.running = False

class App():
    def __init__(self, api):
        self.api = api
        self.threadLock = threading.Lock()
        self.currentPrice = -1
        self.highPrice = -1
        self.lowPrice = -1
        self.volume = -1
        self.bidPrice = -1
        self.askPrice = -1
        self.threads = []
        self.threads.append(monitor(1, "Monitor-1", self))
        self.threads.append(trader(2, "Trader-1", self, 0))
        self.threads.append(trader(3, "Trader-2", self, 1))
        self.threads.append(trader(4, "Trader-3", self, 2))
        self._nonce = int(time.time())

    def start(self):
        spread = 1;
        for t in self.threads:
            t.start()
            time.sleep(spread)
            # Creating increasing spread.
            spread = spread + 33

    def stop(self):
        for t in self.threads:
            t.stop()
        for t in self.threads:
            t.join()

    def getNonce(self):
        currentNonce = self._nonce
        self._nonce += 1
        return currentNonce

class Config():
    def __init__(self, file):
        cfgParser = ConfigParser.ConfigParser()
        cfgParser.read("config.ini")

        self.cid = self.ConfigSectionMap(cfgParser, "Authentication")['cid']
        self.api_key = self.ConfigSectionMap(cfgParser, "Authentication")['key']
        self.API_SECRET = self.ConfigSectionMap(cfgParser, "Authentication")['secret']
        self.apiUrl = "https://www.bitstamp.net/api/"
        self.tradeAmount = 0.1

    def ConfigSectionMap(self, parser, section):
        dict1 = {}
        options = parser.options(section)
        for option in options:
            try:
                dict1[option] = parser.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

# Configure and init the app.
cfg = Config("config.ini")
api = bitstamp.Bitstamp(cfg.apiUrl, cfg.cid, cfg.api_key, cfg.API_SECRET)
app = App(api)

def signalHandler(signal, frame):
    print 'Closing...'
    app.stop()
    print "Bye"
    sys.exit(0)

# Keep running until user presses Ctrl+C
app.start()
signal.signal(signal.SIGINT, signalHandler)
signal.pause()