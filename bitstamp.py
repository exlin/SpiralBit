import urllib
import urllib2
import hmac
import json
import hashlib
import gzip
import zlib
from StringIO import StringIO

class Bitstamp():
    def __init__(self, baseUrl, cid, apiKey, apiSecret):
        self.baseUrl = baseUrl
        self.cid = cid
        self.apiKey = apiKey
        self.apiSecret = apiSecret
    
    def pullPrice(self):
        url = self.baseUrl + "ticker"
        #data = urllib.urlencode(parameters)
        req = urllib2.Request(url)
        req.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            json_object = json.load(data)
        else:
            json_object = json.load(response)
        return json_object

    def sign(self, nonce):
        message = str(nonce) + self.cid + self.apiKey
        signature = hmac.new(self.apiSecret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        return signature

    def getBalance(self, nonce):
        balanceUrl = self.baseUrl + "balance"
        parameters = {}
        parameters['key'] = self.apiKey
        parameters['signature'] = self.sign(nonce)
        parameters['nonce'] = nonce
        #parameters = [('key', self.apiKey),
        #('signature', self.sign(nonce)),
        #('nonce', nonce),
        #]
        data = urllib.urlencode(parameters)
        req = urllib2.Request(balanceUrl, data)
        req.add_header('Accept-Encoding', 'gzip')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            json_object = json.load(data)
        else:
            json_object = json.load(response)
        return json_object

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
        #parameters = [('key', self.apiKey),
        #('signature', self.sign(nonce)),
        #('nonce', nonce),
        #('amount', amount),
        #('price', price),
        #]
        parameters = {}
        parameters['key'] = self.apiKey
        parameters['signature'] = self.sign(nonce)
        parameters['nonce'] = nonce
        parameters['amount'] = amount
        parameters['price'] = price
        
        data = urllib.urlencode(parameters)
        req = urllib2.Request(buyUrl, data)
        req.add_header('Accept-encoding', 'gzip')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            json_object = json.load(data)
        else:
            json_object = json.load(response)
        return json_object

    def sellBitcoins(self, nonce, amount, price):
        sellUrl = self.baseUrl + "sell"
        #parameters = [('key', self.apiKey),
        #('signature', self.sign(nonce)),
        #('nonce', nonce),
        #('amount', amount),
        #('price', price),
        #]
        parameters = {}
        parameters['key'] = self.apiKey
        parameters['signature'] = self.sign(nonce)
        parameters['nonce'] = nonce
        parameters['amount'] = amount
        parameters['price'] = price
        data = urllib.urlencode(parameters)
        req = urllib2.Request(sellUrl, data)
        req.add_header('Accept-encoding', 'gzip')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            json_object = json.load(data)
        else:
            json_object = json.load(response)
        return json_object


    def balanceCheckUSD(self, nonce, amount, price):
        balance = self.getBalance(nonce)['usd_available']
        
        check = False
        ask = float(amount) * float(price)
        if balance > ask:
            check = True

        return check



