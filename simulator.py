from base_objects.orderbook import OrderBook, Order, Side
from base_objects.logger import Logger

class Simulator:

    def __init__(self) -> None:
        
        super().__init__()

        self.logger = Logger('SIMULATOR')
        self.orderbook = OrderBook()

    def run_detection(self):

        pass

    def convert_to_order(self, order_str: str) -> Order:
        
        order_dets = order_str.split(' ')

        return Order(
            Side.BUY if order_dets[1] == 'B' else Side.SELL,
            float(order_dets[2]),
            int(order_dets[3]),
            user_id=order_dets[0]
        )

    def add_new_order(self, order_str: str):

        order = self.convert_to_order(order_str=order_str)
        self.orderbook.process_order(order)
        self.run_detection()

    def populate_orderbook(self, orders: list):

        for order in orders:
            print(order)
            self.orderbook.unprocessed_orders.put(order)

        while not self.orderbook.unprocessed_orders.empty():
            self.orderbook.process_order(self.orderbook.unprocessed_orders.get())


if __name__ == '__main__':

    # Initial orderbook population
    # Estimated mid price at 12.24
    orders = [
        Order(Side.BUY, 12.23, 10, user_id = 'A'),
        Order(Side.BUY, 12.31, 20, user_id = 'B'),
        Order(Side.SELL, 13.55, 5, user_id = 'B'),
        Order(Side.BUY, 12.23, 5, user_id = 'C'),
        Order(Side.BUY, 12.25, 15, user_id = 'A'),
        Order(Side.SELL, 13.31, 5, user_id = 'B'),
        Order(Side.BUY, 12.25, 30, user_id = 'D'),
        Order(Side.SELL, 13.31, 5, user_id = 'A'),
        Order(Side.BUY, 12.23, 10, user_id = 'B')
    ]

    sim = Simulator()

    sim.populate_orderbook(orders = orders)

    sim.orderbook.show_book()
    
    print(sim.orderbook.calculate_fair_price())

    while(True):

        sim.logger.log_info('STOP TO END')
        sim.logger.log_info('Enter order: ')
        order_str = input()
        if order_str == 'STOP':
            break

        sim.add_new_order(order_str = order_str)
        sim.orderbook.show_book()
        
        print(sim.orderbook.calculate_fair_price())