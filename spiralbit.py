import signal
import sys
import time
import threading
import ConfigParser
import bitstamp

class trader (threading.Thread):
    def __init__(self, threadID, name, app):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
        self.app = app
        self.pollInterval = 5
    
    def run(self):
        self.running = True
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        while self.running == True:
            if self.app.currentPrice > -1:
                print "Trading with price " + str(self.app.currentPrice)
                print "Nonce for my next api call is: " + str(self.app.getNonce())
            else:
                print "Price not available."
            time.sleep(self.pollInterval)
        print "Exiting " + self.name

    def stop(self):
        self.running = False

class monitor (threading.Thread):
    def __init__(self, threadID, name, app):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
        self.pollInterval = 10
        self.app = app
    
    def run(self):
        self.running = True
        print "Starting " + self.name
        while self.running == True:
            #Get the last price for trading.
            self.app.currentPrice = self.app.api.pullPrice()['last']
            time.sleep(self.pollInterval)
        print "Exiting " + self.name

    def stop(self):
        self.running = False

class App():
    def __init__(self, api):
        self.api = api
        self.threadLock = threading.Lock()
        self.currentPrice = -1
        self.threads = []
        self.threads.append(monitor(1, "Monitor-1", self))
        self.threads.append(trader(2, "Trader-1", self))
        self.threads.append(trader(3, "Trader-2", self))
        self._nonce = int(time.time())

    def start(self):
        for t in self.threads:
            t.start()

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