import random
import time
from copy import deepcopy

from base_objects.orderbook import OrderBook
from base_objects.logger import Logger
from ramping.ramping import Ramping
from momentum_ignition.momentum_ignition import MomentumIgnition

class Simulator(Logger):

    def __init__(self) -> None:
        
        super().__init__(control_name='SIMULATOR')

        self.orderbook = OrderBook('BTC')

        self.ramping = Ramping()
        self.momentum_ignition = MomentumIgnition()
        # self.wash_trade = WashTrade()
        # self.frontrunning = FrontRunning()

        self.traders = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F'
        ]

    def run_detections(self, old_orderbook, new_orderbook, order):

        # self.ramping.run_detection(old_orderbook, new_orderbook, order)
        self.momentum_ignition.run_detection(old_orderbook, new_orderbook, order)
        

    def make_market(
        self, 
        order_limit = 100,
        qty_start = 500,
        price_start = 500,
        qty_deviation = 100,
        price_deviation = 20
    ):
        
        while(order_limit):

            trader = random.choice(self.traders)
            direction = random.choice([0, 1])
            price = price_start + random.randint(-price_deviation, price_deviation)
            qty = qty_start + random.randint(-qty_deviation, qty_deviation)

            price_start = price
            
            self.orderbook.limit_order(direction, qty, price, trader)
            order_limit -= 1

        print('Market made for currency')
        print(self.orderbook.render())

    def run_random_simulation(
        self, 
        order_limit = 100,
        qty_start = 500,
        price_start = 500,
        qty_deviation = 100,
        price_deviation = 20
    ):

        self.make_market(
            order_limit=order_limit,
            qty_start=qty_start,
            qty_deviation=qty_deviation,
            price_start=price_start,
            price_deviation=price_deviation
        )

        orders = 0
        while orders < 500:

            trader = random.choice(self.traders)
            direction = random.choice([0, 1])
            price = price_start + random.randint(-price_deviation, price_deviation)
            qty = qty_start + random.randint(-qty_deviation, qty_deviation)
            
            price_start = int((self.orderbook.ask_min + self.orderbook.bid_max) / 2)
            
            old_orderbook = deepcopy(self.orderbook)
            self.orderbook.limit_order(direction, qty, price, trader)
            new_orderbook = deepcopy(self.orderbook)
            
            orders += 1

            if orders % 100 == 0:

                print(self.orderbook.render())
                time.sleep(2)

            self.run_detections(
                old_orderbook = old_orderbook,
                new_orderbook = new_orderbook,
                order = {
                    'direction': direction,
                    'qty': qty,
                    'price': price,
                    'trader': trader
                }
            )


if __name__ == '__main__':

    sim = Simulator()

    # Market params
    order_limit = 100
    qty_start = 500
    price_start = 10
    qty_deviation = 100
    price_deviation = 5

    sim.run_random_simulation()
