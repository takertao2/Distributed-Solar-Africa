from heapq import heappush, heappop


class Market:
    _bid = []
    _ask = []
    last_price = 70
    central = None

    def ask(self, token):
        token.put_on_market()
        if len(self._bid) and self._bid[-1][0] >= self.last_price - .01:
            price, quantity, buyer = self._bid[-1]
            self.transaction(token, buyer, price)
            if quantity == 1:
                heappop(self._bid)
            else:
                self._bid[-1] = (price, quantity-1, buyer)
            return True
        heappush(self._ask, (self.last_price*.98, token))
        return False

    def bid(self, villager, quantity):
        bid_price = self.last_price + 0.01
        while len(self._ask) and self._ask[0][0] <= bid_price:
            price, token = heappop(self._ask)
            self.transaction(token, villager, price)
            villager.debit(price)
        villager.debit(bid_price)
        heappush(self._bid, (bid_price, quantity, villager))

    def pull_from_ask(self, token):
        for i in range(len(self._ask)):
            if self._ask[i][1] == token:
                self._ask[i:i+1] = []
                return
        raise Exception("Token not found")

    def transaction(self, token, buyer, price):
        owner = token.owner
        owner.credit(price*.0001)
        owner.remove_token(token)
        buyer.add_token(token)
        token.remove_from_market()
        self.last_price = price
        self.central.bank += price*.0001

    def clean(self):
        for i in self._bid:
            i[2].debit(i[0]*i[1])
        self._bid = []
