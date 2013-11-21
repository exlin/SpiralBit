import json
import urllib
import urllib2
import time

def pullPrice():
    url = "https://www.bitstamp.net/api/ticker"

    #data = urllib.urlencode(parameters)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    json_object = json.load(response)

    print json_object

while True:
    pullPrice()
    time.sleep(10)