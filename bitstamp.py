import urllib
import urllib2
import hmac
import json

class Bitstamp():
    def __init__(self, baseUrl, cid, apiKey, apiSecret):
        self.baseUrl = baseUrl
        self.cid = cid
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def pullPrice(self):
        print "Pulling price..."
        url = self.baseUrl + "ticker"
        #data = urllib.urlencode(parameters)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return json.load(response)

    def sign(self, nonce):
        message = nonce + self.cid + self.apiKey
        signature = hmac.new(self.apiSecret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        return signature

    def getBalance(self, nonce):
        balanceUrl = self.baseUrl + "balance"
        parameters = {"key": api_key,
        "signature": self.sign(nonce),
        "nonce": nonce}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(balanceUrl, data)
        response = urllib2.urlopen(req)
        balance = response.read()
        return balance