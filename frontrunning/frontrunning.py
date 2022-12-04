import time
from mimetypes import init
from base_objects.logger import Logger
from base_objects.orderbook import Order, OrderBook

class FrontRunning:

    def __init__(self) -> None:
        
        super().__init__()

        self.logger = Logger('FR')
        self.user_log = dict()
        
        # Thresholds
        self.frontrunning_interval = 50
        self.perceived_profit_threshold = 100
        self.large_order_thresh = 50

    def run_detection(self, old_orderbook, new_orderbook, order):

        if self.is_large_order(new_orderbook, order):
            user_profits = self.calculate_profits(order)
            for user in user_profits:
                if user_profits[user] > self.perceived_profit_threshold:
                    print('Frontrunning detected!')
        
        if order['order_id'] % self.frontrunning_interval == 0:
            self.user_log.clear()
        
        if order['trader'] in self.user_log.keys():
            order['order_id'] = new_orderbook.order_id
            self.user_log[order['trader']].append(order)
        else:
            order['order_id'] = new_orderbook.order_id
            self.user_log[order['trader']] = [(order)]
    
    def is_large_order(self, orderbook, order):

        if order['qty'] > self.large_order_thresh:
            return True
        return False

    def calculate_profits(self, new_order):

        user_profits = {}

        for user in self.user_log:
            profit = 0
            for order in self.user_log[user]:
                profit += new_order['price'] - order['price']
            user_profits[user] = profit
        return user_profits