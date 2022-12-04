import time
from mimetypes import init
from base_objects.logger import Logger
from base_objects.orderbook import Order, OrderBook

class MomentumIgnition:

    def __init__(self) -> None:
        
        super().__init__()

        self.logger = Logger('MI')
        self.user_log = dict()
        self.user_activity = dict()
        self.init_price = 0
        
        # Thresholds
        self.tau = 0.6
        self.order_window = 20
        self.momentum_interval = 50

    def run_detection(self, old_orderbook, new_orderbook, order):

        if order['direction'] == 0 and order['price'] > new_orderbook.ask_min or order['direction'] == 1 and order['price'] < new_orderbook.bid_max:
            
            if order['trader'] in self.user_log.keys():
                self.user_log[order['trader']] += 1
                order['order_id'] = new_orderbook.order_id
                self.user_activity[order['trader']].append(order)
            else:
                self.user_log[order['trader']] = 1
                order['order_id'] = new_orderbook.order_id
                self.user_activity[order['trader']] = [(order)]

            if new_orderbook.order_id % self.momentum_interval == 0:

                for user in self.user_log.keys():

                    if self.user_log[user] / self.order_window > self.tau:
                        print('Momentum Ignition detected due to user {}.'.format(user))
                        print(self.user_activity[user])
                        time.sleep(10)

                self.user_log.clear()
                self.user_activity.clear()