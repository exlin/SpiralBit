import json
import urllib
import urllib2
import time
import threading

class trader (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

class monitor (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        pullPrice()
        print "Exiting " + self.name

def pullPrice():
    while True:
        url = "https://www.bitstamp.net/api/ticker"
        #data = urllib.urlencode(parameters)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        price = json.load(response)
        time.sleep(10)

threadLock = threading.Lock()
threads = []

# Create new threads
monitor1 = monitor(1, "Monitor-1")
trader1 = trader(1, "Trader-1")
trader2 = trader(2, "Trader-2")

# Start new Threads
monitor1.start()
trader1.start()
trader2.start()



# Add threads to thread list
threads.append(monitor1)
threads.append(trader1)
threads.append(trader2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"