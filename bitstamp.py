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

    def getTransactions(self, nonce, limit=100, offset=0, sort="desc"):
        transactionsUrl = self.baseUrl + "user_transactions"
        parameters = {"key": api_key,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "offset": offset,
        "limit": limit,
        "sort": sort}
        data = urllib.urlencode(parameters)
        req = url.Request(transactionsUrl, data)
        response = urllib2.urlopen(req)
        transactions = response.read()
        return transactions

    def getOpenOrders(self, nonce):
        openordersUrl = self.baseUrl + "open_orders"
        parameters = {"key": api_key,
        "signature": self.sign(nonce),
        "nonce": nonce}
        data = urllib.urlencode(parameters)
        req = url.Request(openordersUrl, data)
        response = urllib2.urlopen(req)
        orders = response.read()
        return orders

    def cancelOrder(self, nonce, orderid):
        cancelUrl = self.baseUrl + "cancel_order"
        parameters = {"key": api_key,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "id": orderid}
        data = urllib.urlencode(parameters)
        req = url.Request(cancelUrl, data)
        response = urllib2.urlopen(req)
        cancelled = response.read()
        return cancelled

    def buyBitcoins(self, nonce, amount, price):
        buyUrl = self.baseUrl + "cancel_order"
        parameters = {"key": api_key,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "amount": amount,
        "price": price}
        data = urllib.urlencode(parameters)
        req = url.Request(buyUrl, data)
        response = urllib2.urlopen(req)
        buy = response.read()
        return buy


