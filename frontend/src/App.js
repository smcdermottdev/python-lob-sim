import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [orderBook, setOrderBook] = useState({ bids: [], asks: [] });

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/book');
        const data = await response.json();
        setOrderBook(data);
      } catch (error) {
        console.error("Error fetching book:", error);
      }
    };

    fetchBook();

    const interval = setInterval(fetchBook, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>🚀 HFT Limit Order Book</h1>
      <h2>Symbol: {orderBook.symbol || "Loading..."}</h2>

      <div style={{ display: "flex", justifyContent: "center", gap: "50px" }}>
        
        <div>
          <h3 style={{ color: "green" }}>BIDS (Buy)</h3>
          {orderBook.bids.length === 0 ? <p>No Bids</p> : (
            <table border="1" cellPadding="10">
              <thead>
                <tr>
                  <th>Price</th>
                  <th>Qty</th>
                </tr>
              </thead>
              <tbody>
                {orderBook.bids.map((level, index) => (
                  <tr key={index}>
                    <td style={{ color: "green", fontWeight: "bold" }}>
                        ${level.price.toFixed(2)}
                    </td>
                    <td>{level.qty}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div>
          <h3 style={{ color: "red" }}>ASKS (Sell)</h3>
          {orderBook.asks.length === 0 ? <p>No Asks</p> : (
            <table border="1" cellPadding="10">
              <thead>
                <tr>
                  <th>Price</th>
                  <th>Qty</th>
                </tr>
              </thead>
              <tbody>
                {orderBook.asks.map((level, index) => (
                  <tr key={index}>
                    <td style={{ color: "red", fontWeight: "bold" }}>
                        ${level.price.toFixed(2)}
                    </td>
                    <td>{level.qty}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;