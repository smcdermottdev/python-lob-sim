from src.core.order import Order, OrderType, Side
from sortedcontainers import SortedDict
from collections import deque 

class OrderBook:
    def __init__(self, symbol: str = "Unknown"):
        self.symbol = symbol
        self.bids = SortedDict()
        self.asks = SortedDict()
        self.id_map = {}

    def add_order(self, order: Order):

        if order.side == Side.BUY: 
            book_side = self.bids    
        else:
            book_side = self.asks
        
        if order.price not in book_side:
            book_side[order.price] = deque()

        book_side[order.price].append(order)

        self.id_map[order.uid] = order
    
    def cancel_order(self, order_id: int):

        if order_id not in self.id_map:
            print(f"Order #{order_id} not found")
            return

        order = self.id_map[order_id]
        
        book_side = self.bids if order.side == Side.BUY else self.asks
        price_deque = book_side[order.price]
        price_deque.remove(order)
        
        if len(price_deque) == 0:
            del book_side[order.price]
            
        del self.id_map[order_id] 

    def get_best_ask(self):
        if not self.asks:
            return None
        else: return self.asks.peekitem(0)[0]

    def get_best_bid(self):
        if not self.bids:
            return None
        else: return self.bids.peekitem(-1)[0]

        
    def process_order(self, order: Order):
        opposite_side = self.bids if order.side == 2 else self.asks
        if opposite_side == self.bids:
            get_best_price = self.get_best_bid
            can_trade = lambda order_price, best_price: best_price >= order_price
        else:
            get_best_price = self.get_best_ask
            can_trade = lambda order_price, best_price: best_price <= order_price
        
        while order.qty > 0 and len(opposite_side) > 0:
            best_price = get_best_price()
            if order.order_type == OrderType.LIMIT and not can_trade(order.price, best_price):
                break 
            opposing_orders_at_price = opposite_side[best_price]
            best_opposing = opposing_orders_at_price[0]
            trade_qty = min(order.qty, best_opposing.qty)
            order.qty -= trade_qty
            best_opposing.qty -= trade_qty


            if best_opposing.qty == 0:
                del self.id_map[best_opposing.uid]
                opposing_orders_at_price.popleft()
            if len(opposing_orders_at_price) == 0:
                del opposite_side[best_price]
        
        if (order.qty > 0) and order.order_type == OrderType.LIMIT:
            self.add_order(order)