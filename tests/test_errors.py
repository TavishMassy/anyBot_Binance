# Import the pytest library to create and run tests
import pytest
# Import tools to replace real parts of the code with fakes for testing
from unittest.mock import AsyncMock, patch
# Import the specific exception class that Binance uses for errors
from binance.exceptions import BinanceAPIException
# Import the client class that connects to the Binance API
from bot.client import BinanceClient
# Import the validator to create a data object for the test
from bot.validators import OrderValidator

# Mark this function as an asynchronous test so it can use 'await'
@pytest.mark.asyncio
async def test_invalid_symbol_error():
    # Replace the actual Binance connection logic with a fake version
    with patch("bot.client.AsyncClient.create", return_value=AsyncMock()):
        # Create an instance of our Binance client
        engine = BinanceClient()
        # Connect to the fake API setup
        await engine.connect()

        # Define a raw JSON error message like the one Binance sends for bad symbols
        error_json = '{"code": -1121, "msg": "Invalid symbol."}'
        # Tell the fake API to raise a BinanceAPIException when an order is placed
        engine.client.futures_create_order.side_effect = BinanceAPIException(None, 400, error_json)

        # Create an order object with a symbol that does not exist
        order = OrderValidator(symbol="INVALID", side="BUY", order_type="MARKET", quantity=1)

        # Verify that our code correctly passes the error up instead of crashing
        with pytest.raises(BinanceAPIException) as excinfo:
            # Try to place the order which we know will trigger the fake error
            await engine.place_order(order)
        
        # Check that the word 'invalid symbol' is actually in the error message
        assert "invalid symbol" in str(excinfo.value).lower()