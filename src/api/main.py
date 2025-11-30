from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.orderbook import OrderBook
from src.core.order import Order, Side, OrderType
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

book = OrderBook("SPY")
print("--- MARKET OPEN: SPY Order Book Initialized ---")

class OrderRequest(BaseModel):
    side: str        
    price: float
    qty: int
    order_type: str 

@app.get("/")
def read_root():
    return {"message": "Trading System Active"}

@app.post("/orders")
def place_order(request: OrderRequest):
    """
    Receives JSON, converts to internal Order object, and sends to engine.
    """
    order_id = int(time.time() * 1000) 
    
    new_order = Order(
        side=Side[request.side.upper()],  
        order_type=OrderType[request.order_type.upper()],
        uid = order_id,
        symbol = "SPY",
        price = request.price,
        qty = request.qty
    )

    book.process_order(new_order)
    
    return {
        "status": "received",
        "order_id": order_id
    }

@app.get("/book")
def get_book():
    """
    Returns the current state of the Order Book (Bids and Asks).
    Used by the Frontend to render the Depth Chart.
    """

    def serialize_side(sorted_dict):
        result = []

        for price, order_deque in sorted_dict.items():
            total_qty = sum(o.qty for o in order_deque)
            result.append({
                "price": price,
                "qty": total_qty,
                "order_count": len(order_deque)
            })
        
        return result

    return {
        "symbol": book.symbol,
        "bids": serialize_side(book.bids)[::-1], 
        "asks": serialize_side(book.asks)
    }