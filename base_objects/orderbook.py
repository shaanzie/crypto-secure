from io import StringIO
from collections import deque, namedtuple

class Order:
    def __init__(self, side, size, price, trader, order_id):

        self.side = side
        self.size = size
        self.price = price
        self.trader = trader
        self.order_id = order_id

class OrderBook(object):
    def __init__(self, name, max_price=10000, start_order_id=0, cb=None):

        self.name = name
        self.order_id = start_order_id
        self.max_price = max_price
        #self.dec_places = dec_places
        self.cb = cb or self.execute
        self.price_points = [deque() for i in range(self.max_price)] 
        self.bid_max = 0
        self.ask_min = max_price + 1
        self.orders = {} # orderid -> Order
        self.trades = []
        
    def execute(self, trader_buy, trader_sell, price, size):
        self.trades.append({
            'buy_account': trader_buy,
            'sell_account': trader_sell,
            'qty': size,
            'price': price,
            'order_id': self.order_id
        })
        print("EXECUTE: %s BUY %s SELL %s %s @ %d" % (trader_buy, trader_sell, size, self.name, price))
        
    def limit_order(self, side, size, price, trader):
        self.order_id += 1
        if type(price) != int:
            raise ValueError("expected price as int (ticks)")
        #if type(price) == float:
        #    price = int(price * (10**self.dec_places))
        if side == 0: # buy order
            # look for outstanding sell orders that cross with the incoming order
            while price >= self.ask_min:
                entries = self.price_points[self.ask_min]
                while entries:
                    entry = entries[0]
                    if entry.size < size:
                        self.cb(trader, entry.trader, price, entry.size)
                        size -= entry.size
                        entries.popleft()
                    else:
                        self.cb(trader, entry.trader, price, size)
                        if entry.size > size:
                            entry.size -= size
                        else:
                            entries.popleft()
                        self.order_id += 1
                        return self.order_id
                        
                # we have exhausted all orders at the ask_min price point. Move on
                # to the next price level
                self.ask_min += 1

            # if we get here then there is some qty we can't fill, so enqueue the order
            self.order_id += 1
            #order.id = self.order_id
            self.price_points[price].append(Order(side, size, price, trader, self.order_id))
            if self.bid_max < price:
                self.bid_max = price
            return self.order_id

        else: # sell order
            # look for outstanding buy orders that cross with the incoming order
            while price <= self.bid_max:
                entries = self.price_points[self.bid_max]
                while entries:
                    entry = entries[0]
                    if entry.size < size:
                        self.cb(entry.trader, trader, price, entry.size)
                        size -= entry.size
                        entries.popleft()
                    else:
                        self.cb(entry.trader, trader, price, size)
                        if entry.size > size:
                            entry.size -= size
                        else:
                            # entry.size == size
                            entries.popleft()
                        self.order_id += 1
                        #id = self.order_id
                        return self.order_id
                        
                # we have exhausted all orders at the ask_min price point. Move on
                # to the next price level
                self.bid_max -= 1

            # if we get here then there is some qty we can't fill, so enqueue the order
            self.order_id += 1
            #order.id = self.order_id
            self.price_points[price].append(Order(side, size, price, trader, self.order_id))
            if self.ask_min > price:
                self.ask_min = price
            return self.order_id	    
            
    def _render_level(self, level, maxlen=40):
        ret = ",".join(("%s:%s(%s)" % (order.size, order.trader, order.order_id) for order in level))
        if len(ret) > maxlen:
            ret = ",".join((str(order.size) for order in level))
        if len(ret) > maxlen:
            ret = "%d orders (total size %d)" % (len(level), sum((order.size for order in level)))
            assert len(ret) <= maxlen
        return ret
        
    def render(self):
        output = StringIO()
        output.write(("-"*110)+"\r\n")
        output.write("Buyers".center(55) + " | " + "Sellers".center(55) + "\r\n")
        output.write(("-"*110)+"\r\n")
        for price in range(self.max_price-1, 0, -1):
            level = self.price_points[price]
            if level:
                if price >= self.ask_min:
                    left_price = ""
                    left_orders = ""
                    right_price = str(price)
                    right_orders = self._render_level(level)
                else:
                    left_price = str(price) 
                    left_orders = self._render_level(level)
                    right_price = ""
                    right_orders = ""
                output.write(left_orders.rjust(43))
                output.write(" |")
                output.write(left_price.rjust(10))
                output.write(" | ")
                output.write(right_price.rjust(10))
                output.write("| ")
                output.write(right_orders.ljust(43))
                output.write("\r\n"+("-"*110)+"\r\n")
        return output.getvalue()

    def calculate_fair_price(self):

        fair_price = 0
        midprice = (self.ask_min + self.bid_max) / 2
        vol = 0
        
        for price in range(self.max_price-1, 0, -1):
            level = self.price_points[price]
            for order in level:

                deficit = midprice - order.price
                fair_price += order.price * order.size
                vol += order.size
        
        return fair_price / vol