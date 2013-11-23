import math

class ActionResponse():
    def __init__(self):
        self.action = "wait" # Modes are wait, sell, buy
        self.price = 0.0

class TradeManager():
    def __init__(self):
        self.mode = 1
    
    def decideBuy(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousPrice):
        response = ActionResponse()
        
        if actedPrice < 1:
            return response
        
        # Check if rate is going up.
        if previousPrice < currentPrice:
        
            # Check that new buy in is 2% lower than the price where we sold previous bitcoins.
            current = ask * 102;
            acted = actedPrice * 100
            if current < acted:
                response.action = "buy"
                response.price = math.ceil(ask*100)/100
        
        return response
    

    def decideSell(self, currentPrice, highPrice, lowPrice, volume, bid, ask, actedPrice, previousPrice):
        response = ActionResponse()
        
        if actedPrice < 1:
            return response
        
        # We think selling once we have just gone past the peak.
        if previousPrice > currentPrice:
            # Check if we would have potential to make profit if we sell it now.
            currentBid = bid * 100
            acted = actedPrice * 101 # x100 + 1% bitstamp fee + 4% profit margin gain.
            
            if currentBid > acted:
                response.action = "sell"
                response.price = math.floor(bid*100)/100
        
        return response