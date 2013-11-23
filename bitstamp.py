import urllib
import urllib2
import hmac
import json
import hashlib

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
        message = str(nonce) + self.cid + self.apiKey
        signature = hmac.new(self.apiSecret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        return signature

    def getBalance(self, nonce):
        balanceUrl = self.baseUrl + "balance"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(balanceUrl, data)
        response = urllib2.urlopen(req)
        return json.load(response)

    def getTransactions(self, nonce, limit=100, offset=0, sort="desc"):
        transactionsUrl = self.baseUrl + "user_transactions"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "offset": offset,
        "limit": limit,
        "sort": sort}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(transactionsUrl, data)
        response = urllib2.urlopen(req)
        transactions = response.read()
        return transactions

    def getOpenOrders(self, nonce):
        openordersUrl = self.baseUrl + "open_orders"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(openordersUrl, data)
        response = urllib2.urlopen(req)
        orders = response.read()
        return orders

    def cancelOrder(self, nonce, orderid):
        cancelUrl = self.baseUrl + "cancel_order"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "id": orderid}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(cancelUrl, data)
        response = urllib2.urlopen(req)
        cancelled = response.read()
        return cancelled

    def buyBitcoins(self, nonce, amount, price):
        buyUrl = self.baseUrl + "buy"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "amount": amount,
        "price": price}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(buyUrl, data)
        response = urllib2.urlopen(req)
        buy = response.read()
        return buy

    def sellBitcoins(self, nonce, amount, price):
        sellUrl = self.baseUrl + "sell"
        parameters = {"key": self.apiKey,
        "signature": self.sign(nonce),
        "nonce": nonce,
        "amount": amount,
        "price": price}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(sellUrl, data)
        response = urllib2.urlopen(req)
        sell = response.read()
        return sell

    def balanceCheckUSD(self, nonce, amount, price):
        balance = self.getBalance(nonce)['usd_available']
        print "Printing"
        print amount
        print price
        
        check = False
        ask = amount * price
        if balance > ask:
            check = True

        return check



