from dataclasses import dataclass, field
from enum import IntEnum
import time



class Side(IntEnum):
    BUY = 1
    SELL = 2

class OrderType(IntEnum):
    MARKET = 1
    LIMIT = 2

@dataclass(slots=True)
class Order:
    side: Side
    order_type: OrderType
    uid: int
    symbol: str
    price: float
    qty: int
    timestamp: float = field(default_factory=time.time)


import random

# A simple counter to give every order a unique ID
_order_id_counter = 0

def generate_random_order(symbol="SPY") -> Order:
    global _order_id_counter
    _order_id_counter += 1
    
    # 1. Randomize Side (Buy or Sell)
    side = random.choice(list(Side))
    
    # 2. Randomize Price (e.g., between $100 and $105)
    # round(..., 2) mimics real tick sizes (pennies)
    price = round(random.uniform(100.00, 105.00), 2)
    
    # 3. Randomize Quantity (e.g., 10, 50, 100 shares)
    qty = random.randint(1, 10) * 10
    
    return Order(
        uid=_order_id_counter,
        symbol=symbol,
        side=side,
        order_type=OrderType.LIMIT,
        price=price,
        qty=qty
    )

# --- Test it immediately ---
if __name__ == "__main__":
    print("--- Generating Fake Market Data ---")
    for _ in range(5):
        print(generate_random_order())
