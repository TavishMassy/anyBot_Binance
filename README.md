
---

# Binance Futures Trading Bot

### Project Overview
This is a Python application built to place orders on the Binance Futures Testnet (USDT-M). The bot supports Market, Limit, and Stop-Market orders. It is designed with a clear separation between the user interface and the trading logic.

---

### Setup Steps

1. **Get the Code**
   Download and unzip the project folder or clone the repository to your computer.

2. **Create a Virtual Environment**
   Open your terminal in the project folder and run these commands to keep the project libraries separate from your system:
   ```bash
   python -m venv .venv
   # On Windows run:
   .venv\Scripts\activate
   # On Mac or Linux run:
   source .venv/bin/activate
   ```

3. **Install Required Libraries**
   Install the necessary packages listed in the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Credentials**
   Create a new file in the root folder named `.env`. Inside that file, add your Binance Testnet keys exactly like this:
   ```text
   BINANCE_API_KEY=your_actual_testnet_api_key
   BINANCE_API_SECRET=your_actual_testnet_api_secret
   ```

---

### How to Run Examples

To start the bot, run the following command:
```bash
python main.py
```

**Example 1: Placing a Market Order**
1. Run the script and follow the prompts.
2. Enter `BTCUSDT` for the symbol.
3. Enter `B` for a Buy order.
4. Enter `M` for Market type.
5. Enter the quantity (for example: `0.001`).

**Example 2: Placing a Limit Order**
1. Run the script.
2. Enter `BTCUSDT`.
3. Enter `S` for a Sell order.
4. Enter `L` for Limit type.
5. Enter the quantity and the Price you want to sell at (for example: `75000`).

---

### Automated Testing Details

To verify the code quality and logic, you can run the test suite using the following command:

```bash
python -m pytest --cov=bot tests/
```

**The test suite covers the following areas:**

* **API Client Logic (`test_client.py`)**: Mocks the Binance API to verify that the bot sends the correct parameters (like `stopPrice` and `workingType`) to the exchange.
* **Error Handling (`test_errors.py`)**: Simulates a "Binance API Exception" (such as an invalid symbol) to prove that the bot handles exchange errors gracefully without crashing.
* **Execution Lifecycle (`test_orders.py`)**: Verifies the full workflow of a trade, ensuring the bot successfully connects, places the order, and then closes the network connection.
* **Input Validation (`test_validators.py`)**: Checks that the bot correctly blocks "bad" data. For example, it ensures a Limit order is rejected if a price is missing, and a Stop-Market order is rejected if a trigger price is missing.

---

### Project Assumptions

1. **Testnet Environment**: This bot is hard-coded to connect only to the Binance Futures Testnet to ensure no real money is ever at risk.
2. **Asset Type**: The bot is designed specifically for USDT-M (USDT-margined) futures contracts.
3. **Price Triggers**: For Stop-Market orders, the bot uses the "Mark Price" as the trigger to protect against market volatility.
4. **Data Formatting**: Numerical inputs are converted to strings before being sent to the API to avoid floating-point math errors.

---

### Project Structure

* **bot/client.py**: Handles the network connection and communication with Binance.
* **bot/orders.py**: Manages the flow of placing a trade and closing the connection.
* **bot/validators.py**: Uses Pydantic to check user input for symbols and numbers.
* **bot/logger.py**: Saves all actions and errors to the `logs/trading_bot.log` file.
* **main.py**: The main entry point that provides the interactive terminal menu.
* **tests/**: Contains automated tests to verify the client, errors, and validation rules.

---
