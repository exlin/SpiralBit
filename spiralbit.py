import signal
import sys
import time
import threading
import ConfigParser
import bitstamp

threads = []

class trader (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
    def run(self):
        self.running = True
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        while self.running == True:
            doTrading()
            time.sleep(5)
        print "Exiting " + self.name
    def stop(self):
        self.running = False

class monitor (threading.Thread):
    def __init__(self, threadID, name, pollInterval, api):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = False
        self.pollInterval = pollInterval
        self.api = api
    def run(self):
        self.running = True
        print "Starting " + self.name
        while self.running == True:
            api.pullPrice()
            time.sleep(10)
        print "Exiting " + self.name
    def stop(self):
        self.running = False

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def doTrading():
    print "Trading..."



def signalHandler(signal, frame):
    print 'Closing...'
    for t in threads:
        t.stop()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Bye"
    sys.exit(0)

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

cid = ConfigSectionMap("Authentication")['cid']
api_key = ConfigSectionMap("Authentication")['key']
API_SECRET = ConfigSectionMap("Authentication")['secret']
apiUrl = "https://www.bitstamp.net/api/"

threadLock = threading.Lock()
api = bitstamp.Bitstamp(apiUrl, cid, api_key, API_SECRET)

# Create new threads
monitor1 = monitor(1, "Monitor-1", 10, api)
trader1 = trader(2, "Trader-1")
trader2 = trader(3, "Trader-2")

# Start new Threads
#monitor1.start()
#trader1.start()
#trader2.start()

# Add threads to thread list
threads.append(monitor1)
threads.append(trader1)
threads.append(trader2)

# Let's start
for t in threads:
    t.start()

# Keep running until users presses Ctrl+C
signal.signal(signal.SIGINT, signalHandler)
signal.pause()