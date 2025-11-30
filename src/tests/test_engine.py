import sys
from pathlib import Path

# CALCULATION
current_file = Path(__file__).resolve()
root_dir = current_file.parents[2]
sys.path.append(str(root_dir))

# ... imports ...

from src.core.order import Side, OrderType, Order
from src.core.orderbook import OrderBook

def test_market_sweep():
    """
    Verifies that an aggressive BUY order correctly 'sweeps' through 
    multiple price levels in the Order Book.
    
    Checks:
    1. Full consumption of the best price level ($100).
    2. Partial consumption of the next price level ($101).
    3. Proper cleanup of empty price levels (memory management).
    """
    print("--- Starting Sweep Test ---")
    

    book = OrderBook("SPY")
    
    # add seller 1/liquidity
    sell1 = Order(uid=1, symbol="SPY", side=Side.SELL, order_type=OrderType.LIMIT, price=100.00, qty=10)
    book.add_order(sell1)
    
    # add seller 2
    sell2 = Order(uid=2, symbol="SPY", side=Side.SELL, order_type=OrderType.LIMIT, price=101.00, qty=10)
    book.add_order(sell2)
    
    print(f"Initial Asks: {[f'{o.qty}@{o.price}' for price in book.asks.values() for o in price]}")
    # Expected: ['10@100.0', '10@101.0']

    # 3 create buyer order
    buy_order = Order(uid=3, symbol="SPY", side=Side.BUY, order_type=OrderType.LIMIT, price=102.00, qty=15)
    
    print(f"\nIncoming Buy Order: {buy_order.qty} shares @ {buy_order.price}")
    book.process_order(buy_order)

    # 4 verification
    print("\n--- Results ---")
    
    if 100.00 not in book.asks:
        print("✅ SUCCESS: $100.00 level cleared.")
    else:
        print("❌ FAIL: $100.00 level still exists.")

    if 101.00 in book.asks:
        remaining_qty = book.asks[101.00][0].qty
        if remaining_qty == 5:
            print("✅ SUCCESS: $101.00 level has 5 shares remaining.")
        else:
            print(f"❌ FAIL: $101.00 level has {remaining_qty} shares (Expected 5).")
    else:
        print("❌ FAIL: $101.00 level is missing.")

    if 1 not in book.id_map and 2 in book.id_map:
        print("✅ SUCCESS: ID Map correctly updated.")
    else:
        print(f"❌ FAIL: ID Map dirty. Keys: {list(book.id_map.keys())}")

if __name__ == "__main__":
    test_market_sweep()