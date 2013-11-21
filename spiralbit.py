import json
import urllib
import urllib2

def pullPrice():
    url = "https://www.bitstamp.net/api/ticker"

    #data = urllib.urlencode(parameters)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    json_object = json.load(response)

    print json_object

pullPrice()