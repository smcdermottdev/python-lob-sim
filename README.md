# Python Limit Order Book (LOB) implementation

A pure Python implementation of a High-Frequency Trading (HFT) Matching Engine.
Designed to verify logic for a future C++ implementation.

## Features
* **Price-Time Priority Matching**
* **O(1) Order Execution** (using Deques)
* **O(1) Cancellation** (using Hash Maps)
* **Memory Safe** (Auto-cleanup of empty price levels)

## How to Run Tests
```bash
python -m src.tests.test_engine