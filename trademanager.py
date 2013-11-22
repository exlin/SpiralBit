import math

class ActionResponse():
    def __init__(self):
        self.action = "wait" # Modes are wait, sell, buy
        self.price = 0.0

class TradeManager():
    def __init__(self):
        self.mode = 1
    
    def decideBuy(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousPrice):
        print "Thinking..."
        response = ActionResponse()
        response.action = "wait"
        response.price = 0
        return response
    

    def decideSell(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousPrice):
        print "Thinking..."
        response.action = "wait"
        response.price = 0
        return response