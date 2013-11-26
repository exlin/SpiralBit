import math

class ActionResponse():
    def __init__(self):
        self.action = "wait" # Modes are wait, sell, buy
        self.price = 0.0

class TradeManager():
    def __init__(self):
        self.mode = 1
    
    def decideBuy(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousAsk):
        response = ActionResponse()
        
        if actedPrice < 20.25:
            print "Price error, actedprice" + str(actedprice)
        
        ask = float(ask)
        actedPrice = float(actedPrice)
        previousAsk = float(previousAsk)
                
        # Check if rate is going up or if we can secure coins $23 cheaper than we sold them.
        if previousAsk < ask or ask+23 < actedPrice:
        
            # Check that new buy in is 2% lower than the price where we sold previous bitcoins.
            current = float(ask) * 1.01
            acted = float(actedPrice)
            if current < acted:
                response.action = "buy"
                response.price = float(ask) + float(0.01)
                print "Purcase made because it made sence"
        
        return response
    

    def decideSell(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousBid, profit, holdHigh):
        response = ActionResponse()
        if actedPrice < 20.25:
            print "Price error, actedprice " + str(actedPrice)
            return response
        
        bid = float(bid)
        actedPrice = float(actedPrice)
        previousBid = float(previousBid)
        holdHigh = float(holdHigh)
        
        # We think selling once we have just gone past the peak over $4.
        if previousBid > bid and float(bid + 4) < holdHigh:
            # Check if we would have potential to make profit if we sell it now.
            currentBid = float(bid) * float(100.00)
            aim = 101 + profit
            acted = float(actedPrice) * float(aim)
            
            if currentBid > acted:
                response.action = "sell"
                response.price = float(bid) - float(0.01)
                profit = float(response.price)- float(actedPrice)
                print "Sold with profit " + str(profit)
    
        return response