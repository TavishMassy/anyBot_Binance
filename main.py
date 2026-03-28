# Import the asyncio library to run asynchronous tasks
import asyncio
# Import the typer library to build the terminal command line interface
import typer
# Import the function that handles placing the actual order
from bot.orders import execute_order
# Import the validator class to check user inputs
from bot.validators import OrderValidator
# Import the logger to record events to a file
from bot.logger import log

# Create a Typer app instance to handle the command line commands
app = typer.Typer()

# Define an asynchronous function to act as a bridge for the trading logic
async def process_trade(order_request):
    # Use a logging context to tag logs with the specific trading symbol
    with log.contextualize(order=order_request.symbol):
        # Print a message to the terminal showing the connection starting
        typer.echo(f"Connecting to Binance for {order_request.order_type}...")
        
        # Call the execute function and wait for the response from the API
        response = await execute_order(order_request)
        
        # Return the data received from Binance back to the main loop
        return response

# Define the main command that starts when the script is run
@app.command()
def main():
    # Print a startup message to the terminal
    typer.secho("Trading Terminal Active. Press Ctrl+C to stop.", fg=typer.colors.CYAN, bold=True)

    # Start an infinite loop so the program stays open for multiple trades
    while True:
        try:
            # Print a visual separator line for a new order
            typer.secho("\n" + "="*30, fg=typer.colors.BRIGHT_BLACK)
            # Print a header for the order configuration section
            typer.secho("NEW ORDER CONFIGURATION", fg=typer.colors.BRIGHT_MAGENTA, bold=True)
            
            # Ask the user for the symbol and default to BTCUSDT if they press enter
            symbol = typer.prompt("Symbol", default="BTCUSDT").upper()

            # Ask for the side using a single letter shortcut for speed
            side_choice = typer.prompt("Side (B for Buy / S for Sell)").upper()
            # Convert the single letter into the full word BUY or SELL
            side = "BUY" if side_choice == "B" else "SELL"

            # Create a map to turn single letters into full order type names
            type_map = {"M": "MARKET", "L": "LIMIT", "S": "STOP_MARKET"}
            # Ask for the type using a shortcut (M, L, or S)
            type_choice = typer.prompt("Type (M for Market / L for Limit / S for Stop)").upper()
            # Get the full type name from the map or default to MARKET
            order_type = type_map.get(type_choice, "MARKET")

            # Ask the user for the quantity as a decimal number
            quantity = typer.prompt("Quantity", type=float)

            # Initialize price variables as empty
            price = None
            stop_price = None

            # If the user chose LIMIT, ask for the specific limit price
            if order_type == "LIMIT":
                price = typer.prompt("Limit Price", type=float)
            # If the user chose STOP_MARKET, ask for the trigger price
            elif order_type == "STOP_MARKET":
                stop_price = typer.prompt("Stop Price", type=float)
            
            # Print a closing separator line
            typer.secho("="*30 + "\n", fg=typer.colors.BRIGHT_BLACK)

            # Pass all gathered inputs into the validator class to check for errors
            order_request = OrderValidator(
                symbol=symbol, side=side, order_type=order_type,
                quantity=quantity, price=price, stop_price=stop_price
            )

            # Use asyncio.run to start the asynchronous trading process from this synchronous loop
            response = asyncio.run(process_trade(order_request))

            # If a response was received, show the success details
            if response:
                # Print a success header in green
                typer.secho("\nORDER SUCCESSFUL", fg=typer.colors.GREEN, bold=True)
                typer.echo("---------------------------")
                # Show the ID returned by Binance
                typer.echo(f"Order ID:  {response.get('orderId', 'N/A')}")
                # Show the current status of the order
                typer.echo(f"Status:    {response.get('status', 'NEW')}")
                typer.echo("---------------------------")

            # Ask the user if they want to enter another trade or quit
            if not typer.confirm("\nPlace another trade?"):
                # Print a exit message and break the loop to close the app
                typer.echo("Shutting down systems... Goodbye!")
                break

        except Exception as e:
            # If any error happens, print it in red
            typer.secho(f"\nERROR: {str(e)}", fg=typer.colors.RED)
            # Ask if the user wants to try again or quit the program
            if not typer.confirm("Try again?"):
                break

# Standard Python check to ensure the script runs only when executed directly
if __name__ == "__main__":
    # Start the Typer application
    app()