
---

# System Architecture

This document explains the internal flow of the trading bot and how the different components interact to execute a trade.

### 1. File Responsibilities

* **main.py**: The Entry Point. It handles the user interface and collects data.
* **bot/validators.py**: The Gatekeeper. It ensures data is safe and complete before any logic runs.
* **bot/orders.py**: The Orchestrator. It manages the start-to-finish process of a single trade.
* **bot/client.py**: The Connector. It talks directly to the Binance API.
* **bot/logger.py**: The Auditor. It records every step to a file for review.
* **bot/config.py**: The Vault. It holds the API keys and system settings.

---

### 2. Execution Flow (Step-by-Step)

When you place an order, the request follows this exact path:

**Step A: User Input (main.py)**
1. The user starts the program.
2. The program asks for Symbol, Side, Type, and Quantity.
3. If the type is LIMIT or STOP_MARKET, it also asks for the Price.

**Step B: Data Validation (bot/validators.py)**
1. The raw inputs are passed to the `OrderValidator` class.
2. Pydantic checks if numbers are positive and if strings (like symbols) follow the correct format.
3. The `model_validator` checks if a price was provided for Limit orders or if a stop price was provided for Stop orders.
4. If validation fails, the bot stops and shows an error to the user.

**Step C: Trade Orchestration (bot/orders.py)**
1. The validated data is sent to the `execute_order` function.
2. This function creates a new `BinanceClient` instance.
3. It triggers the `connect()` command.

**Step D: API Communication (bot/client.py)**
1. The client establishes a secure connection to the Binance Testnet using the API keys from the `.env` file.
2. The `place_order` method converts our internal data into the specific JSON format Binance requires.
3. The request is sent over the internet to Binance.

**Step E: Response and Cleanup (bot/orders.py)**
1. Binance sends back a response (Success or Failure).
2. The `execute_order` function logs the result.
3. The `finally` block runs, which forces the `BinanceClient` to disconnect and close the network socket.

**Step F: UI Feedback (main.py)**
1. The final result is returned to the terminal.
2. The bot asks the user if they want to place another trade or quit.

---

### 3. Order Type Differences

* **MARKET Order**: Skips the price requirement and executes immediately at the current exchange price.
* **LIMIT Order**: Requires a `price`. The bot tells Binance to only fill the order at that specific price or better.
* **STOP_MARKET Order**: Requires a `stop_price`. The order stays "inactive" on the exchange until the Mark Price hits the trigger price, at which point it becomes a Market order.

---

### Why this structure was chosen:

* **Reliability**: If the API logic fails, the validator still protects the system from sending bad data.
* **Scalability**: If you wanted to add a Web UI later, you could keep the `bot/` folder exactly the same and only replace `main.py`.
* **Safety**: Closing the connection in the `finally` block ensures the bot does not use unnecessary computer memory or leave open connections.

---
