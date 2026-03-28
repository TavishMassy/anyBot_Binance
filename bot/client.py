# Import the main client for connecting to Binance asynchronously
from binance import AsyncClient
# Import specific error types from the library to handle API failures
from binance.exceptions import BinanceAPIException
# Import the configuration settings like API keys
from bot.config import settings
# Import the logger to save events to a file
from bot.logger import log
# Import the validator to check order data before sending
from bot.validators import OrderValidator

class BinanceClient:
    def __init__(self):
        # Start with no connection
        self.client = None

    async def connect(self):
        # Try to establish a connection
        try:
            # Create the client using keys from settings
            self.client = await AsyncClient.create(
                api_key=settings.API_KEY,
                api_secret=settings.API_SECRET,
                # Use the testnet environment for safe trading
                testnet=True
            )
            # Log that the connection worked
            log.info("Connected to Binance Futures Testnet")
        except Exception as e:
            # Log the error message if connection fails
            log.error(f"Connection Failed: {str(e)}")
            # Stop the program by raising the error
            raise

    async def disconnect(self):
        # Check if a client exists before closing
        if self.client:
            # Close the connection cleanly
            await self.client.close_connection()
            # Log that we have disconnected
            log.info("Disconnected from Binance")

    async def place_order(self, order: OrderValidator):
        # Try to send the order
        try:
            # Create a dictionary of parameters for the API call
            params = {
                # Symbol like BTCUSDT
                "symbol": order.symbol,
                # Either BUY or SELL
                "side": order.side,
                # Either MARKET, LIMIT, or STOP_MARKET
                "type": order.order_type,
                # Convert quantity to a string for the API
                "quantity": str(order.quantity),
            }

            # Add extra parameters if the type is LIMIT
            if order.order_type == "LIMIT":
                # Convert limit price to a string
                params["price"] = str(order.price)
                # Set time in force to Good 'Til Cancelled
                params["timeInForce"] = "GTC"

            # Add extra parameters if the type is STOP_MARKET
            if order.order_type == "STOP_MARKET":
                # Check if stop price was provided
                if order.stop_price is None:
                    # Error if price is missing
                    raise ValueError("Stop price missing for STOP_MARKET order")
                
                # Convert stop price to a string
                params["stopPrice"] = str(order.stop_price)
                # Use the stable mark price as the trigger
                params["workingType"] = "MARK_PRICE"

            # Log the parameters being sent
            log.info(f"Sending {order.order_type} Order: {params}")
            
            # Call the actual Binance API method with our parameters
            response = await self.client.futures_create_order(**params)
            
            # Log success and the unique ID given by Binance
            log.info(f"Order Accepted ID: {response.get('orderId')}")
            # Return the full API response
            return response

        except BinanceAPIException as e:
            # Catch errors specifically from Binance
            log.error(f"Binance API Error: {e.message} (Code: {e.code})")
            # Re-raise the error to be handled by the caller
            raise
        except Exception as e:
            # Catch any other generic system errors
            log.error(f"System Error: {str(e)}")
            # Re-raise the error
            raise