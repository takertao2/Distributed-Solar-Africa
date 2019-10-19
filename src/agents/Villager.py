from .Market import Market
from .functions import scaled_gaussian


class Villager:
    market = Market()

    def __init__(self, morning_scale, evening_scale):
        self.morning_scale = morning_scale
        self.evening_scale = evening_scale
        self.bank = 0
        self.needed_consumption = 0
        self.consumption = 0
        self.tokens = set()
        self.tokens_on_market = set()

    def credit(self, price):
        self.bank += price

    def debit(self, price):
        self.bank -= price

    def add_token(self, token):
        token.owner = self
        self.tokens.add(token)

    def remove_token(self, token):
        self.tokens_on_market.remove(token)

    def sell(self, token):
        self.tokens.remove(token)
        if not Villager.market.ask(token):
            self.tokens_on_market.add(token)

    def buy(self, quantity):
        Villager.market.bid(self, quantity)

    def needed_consumption_update(self, time):
        t = time % 24
        minimum_consumption = .2
        self.needed_consumption = minimum_consumption + self.morning_scale*scaled_gaussian(7, 1.25**2, t) + self.evening_scale*scaled_gaussian(20, 2.5**2, t)
