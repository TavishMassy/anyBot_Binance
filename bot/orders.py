# Import the custom Binance client class to handle connections
from bot.client import BinanceClient
# Import the validator class to ensure the order data is correct
from bot.validators import OrderValidator
# Import the global log instance for recording events
from bot.logger import log
# Import asyncio to handle timing and background tasks
import asyncio

async def execute_order(order_data: OrderValidator):
    # This function manages the start-to-finish process of one trade
    
    # Create an instance of the Binance client
    engine = BinanceClient()
    try:
        # Start the connection to the testnet server
        await engine.connect()
        
        # Send the validated order details to Binance and wait for a response
        response = await engine.place_order(order_data)
        
        # Log that the trade was successfully sent to the exchange
        log.info(f"Trade Finalized: {order_data.symbol} {order_data.side}")
        # Return the response data for the CLI to display
        return response
        
    except Exception as e:
        # Log any errors that happen during the connection or placement
        log.error(f"Execution Interrupted: {str(e)}")
        # Pass the error back up so the main program knows it failed
        raise e
    finally:
        # The finally block runs no matter what, even if an error occurs
        # This ensures the network connection is always closed properly
        await engine.disconnect()

async def watch_order_status(client, symbol, order_id):
    # This function checks a pending order until it is completed or cancelled
    
    # Log that the monitoring process has started
    log.info(f"Watchdog Active: Monitoring Order {order_id}...")
    
    # Loop indefinitely until the order status changes to a final state
    while True:
        try:
            # Request the current status of the order from Binance
            status_resp = await client.client.futures_get_order(
                symbol=symbol, 
                orderId=order_id
            )
            
            # Extract the status string (like NEW, FILLED, or CANCELED)
            current_status = status_resp.get("status")
            
            # If the order is filled, the trade is complete
            if current_status == "FILLED":
                # Log the success
                log.info(f"TARGET HIT! Order {order_id} has been FILLED.")
                # Get the actual price the trade was executed at
                avg_price = status_resp.get("avgPrice")
                # Print the final result to the terminal
                print(f"\nSTOP TRIGGERED: {symbol} bought at avg price {avg_price}")
                # Exit the loop
                break
                
            # If the order is cancelled or expired, stop monitoring
            if current_status in ["CANCELED", "EXPIRED"]:
                # Log the outcome
                log.info(f"Order {order_id} was {current_status}.")
                # Exit the loop
                break
            
            # Wait for 5 seconds before checking the status again
            # This prevents the bot from being banned for too many API requests
            await asyncio.sleep(5)
            
        except Exception as e:
            # Log any technical errors that happen during monitoring
            log.error(f"Watchdog Error: {e}")
            # Exit the loop if an error occurs
            break