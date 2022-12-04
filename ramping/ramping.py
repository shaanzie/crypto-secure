import time
from mimetypes import init
from base_objects.logger import Logger
from base_objects.orderbook import Order, OrderBook

class Ramping:

    def __init__(self) -> None:
        
        super().__init__()

        self.logger = Logger('RAMPING')
        self.user_log = dict()
        self.user_activity = dict()
        self.init_price = 0
        
        # Thresholds
        self.ramp_threshold = 50
        self.user_contribs_threshold = 1

    def run_detection(self, old_orderbook, new_orderbook, order):

        fp_move = new_orderbook.calculate_fair_price() - old_orderbook.calculate_fair_price()
        if order['trader'] in self.user_log.keys():
            self.user_log[order['trader']] += fp_move
            order['order_id'] = new_orderbook.order_id
            self.user_activity[order['trader']].append(order)
        else:
            self.user_log[order['trader']] = fp_move
            order['order_id'] = new_orderbook.order_id
            self.user_activity[order['trader']] = [(order)]

        if new_orderbook.order_id % self.ramp_threshold == 0:

            for user in self.user_log.keys():

                if self.user_log[user] > self.user_contribs_threshold:
                    print('Ramping detected due to user {}.'.format(user))
                    print(self.user_activity[user])
                    time.sleep(10)

            self.user_log.clear()
            self.user_activity.clear()

            return 1