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
        
        # We may want to buy once rate is going up and that change has been at least y%.
        previous = previousPrice * 103;
        current = ask * 100;
        if previous < current:
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
            acted = actedPrice * 105 # x100 + 1% bitstamp fee + 4% profit margin gain.
            
            if currentBid > acted:
                response.action = "sell"
                response.price = math.floor(bid*100)/100
        
        return response