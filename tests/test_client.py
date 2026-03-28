# Import the pytest library to run the automated tests
import pytest
# Import mocking tools to simulate the Binance API without needing real keys
from unittest.mock import AsyncMock, patch
# Import the client class that we want to test
from bot.client import BinanceClient
# Import the validator to create valid order data for the test
from bot.validators import OrderValidator

# Tell pytest that this function is an asynchronous test
@pytest.mark.asyncio
async def test_place_stop_market_order():
    # Replace the real Binance AsyncClient with a fake one (mock)
    with patch("bot.client.AsyncClient.create", return_value=AsyncMock()) as mocked_api:
        # Create an instance of our client
        engine = BinanceClient()
        # Connect to the fake API
        await engine.connect()

        # Set what the fake API should return when the order method is called
        engine.client.futures_create_order.return_value = {
            "orderId": 123456,
            "status": "NEW",
            "symbol": "BTCUSDT"
        }

        # Create a valid stop market order object for testing
        order = OrderValidator(
            symbol="BTCUSDT", side="BUY", order_type="STOP_MARKET", 
            quantity=0.008, stop_price=71000
        )

        # Execute the function that sends the order to the fake API
        response = await engine.place_order(order)
        
        # Verify that the response contains the correct fake order ID
        assert response["orderId"] == 123456
        
        # Verify that our code actually called the Binance API exactly once
        engine.client.futures_create_order.assert_called_once()
        
        # Extract the exact parameters our code sent to the API
        args, kwargs = engine.client.futures_create_order.call_args
        
        # Check that the stop price was converted to a string correctly
        assert kwargs["stopPrice"] == "71000.0"
        # Check that we correctly sent the trigger type as MARK_PRICE
        assert kwargs["workingType"] == "MARK_PRICE"