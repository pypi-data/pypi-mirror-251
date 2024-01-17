import math

from src.tdexchange.client import Exchange
import threading
import time
import random


class Bot:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.thread = None
        self.stopped = False

    def strategy(self, exchange: Exchange):
        raise Exception('bot.strategy not implemented')

    def run(self):
        exchange = Exchange(self.name, self.password)
        exchange.connect()

        def execute():
            while not self.stopped:
                time.sleep(0.25)
                self.strategy(exchange)

            exchange.close()

        self.thread = threading.Thread(target=execute)
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.stopped = True

        self.thread.join()


class MarketPrice:
    def __init__(self, ret: float = 0.001, sd: float = 0.34, initial: float = 20):
        self.ret = ret
        self.sd = sd
        self.price = initial

    def tick(self):
        # simulate the market price by a lognormal random walk
        c = 365 * 24 * 3
        self.price *= (1 + random.normalvariate(self.ret / c, self.sd / math.sqrt(c)))


class PairPrice:
    def __init__(self, target: MarketPrice, var: float = 0.01):
        self.target = target
        self.price = self.target.price
        self.delta = 0
        self.var = var

    def tick(self):
        # simulate the pair price by randomly generating a delta, and linear interpolate towards it
        target = random.normalvariate(0, 0.25 * self.target.price)
        self.delta = self.delta + self.var * (target - self.delta)
        self.price = self.target.price + self.delta


class RegularBot(Bot):

    def __init__(self, name, password, price: MarketPrice, pair: PairPrice):
        super().__init__(name, password)
        self.price = price
        self.pair = pair
        self.tick = 0

    def strategy(self, exchange: Exchange):
        self.tick += 1

        A = 'PHILIPS_A'
        self.price.tick()

        target = self.price.price
        if self.tick % 5 == 0:
            exchange.delete_orders(A)

        # create a boundary of bids and asks around the price
        margin = 0.005 * target
        bid = random.randint(40, 60)
        bid2 = random.randint(190, 210)
        exchange.insert_order(A, target - margin, bid, 'bid', 'limit')
        exchange.insert_order(A, target - 2 * margin, bid2, 'bid', 'limit')
        exchange.insert_order(A, target + margin, bid, 'ask', 'limit')
        exchange.insert_order(A, target + 2 * margin, bid2, 'ask', 'limit')

        B = 'PHILIPS_B'
        self.pair.tick()

        target = self.pair.price
        if self.tick % 3 == 0:
            exchange.delete_orders(B)

        # create a boundary of bids and asks around the price
        margin = 0.01 * target
        ask = random.randint(90, 110)
        ask2 = random.randint(900, 1100)
        exchange.insert_order(B, target - margin, ask, 'bid', 'limit')
        exchange.insert_order(B, target - 2 * margin, ask2, 'bid', 'limit')
        exchange.insert_order(B, target + margin, ask, 'ask', 'limit')
        exchange.insert_order(B, target + 2 * margin, ask2, 'ask', 'limit')
