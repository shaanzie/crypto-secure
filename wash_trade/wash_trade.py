import time
from mimetypes import init
from base_objects.logger import Logger
from base_objects.orderbook import Order, OrderBook

from networkx import DiGraph, simple_cycles

class WashTrade:

    def __init__(self) -> None:
        
        super().__init__()

        self.logger = Logger('WT')
        self.wash_graph = DiGraph()
        
        # Thresholds
        self.wt_thresh = 4
        self.wash_window_threshold = 50

    def run_detection(self, old_orderbook, new_orderbook, trades):
        
        self.wash_graph.clear()

        consider_trades = []
        for trade in trades:
            if trade['order_id'] > new_orderbook.order_id - self.wash_window_threshold:
                consider_trades.append(trade)
                
            edge = self.make_edge(trade)
            self.add_edge(edge)

            if self.cycle_length() > self.wt_thresh:

                print('Wash trading detected!')


    def make_edge(self, trade):

        from_trader = ord(trade['from_trader'])
        to_trader = ord(trade['to_trader'])

        self.wash_graph.add_edge(from_trader, to_trader)

    def cycle_length(self, trade):

        cycles = sorted(simple_cycles(self.wash_graph))
        num_cycles = 0
        for cycle in cycles:
            if trade['from_trader'] in self.wash_graph or trade['to_trader'] in cycle:
                num_cycles += 1
        return num_cycles
