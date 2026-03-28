# Import the pytest library to allow running automated tests
import pytest
# Import mocking tools to replace real components with fake ones for testing
from unittest.mock import AsyncMock, patch
# Import the orchestrator function that manages the trade process
from bot.orders import execute_order
# Import the validator to create a valid data object for the test
from bot.validators import OrderValidator

# Mark this function as an asynchronous test so it can use 'await'
@pytest.mark.asyncio
async def test_execute_order_flow():
    # Replace the BinanceClient class with a fake version (mock)
    with patch("bot.orders.BinanceClient") as MockClient:
        # Get the fake instance that the class will return when created
        mock_instance = MockClient.return_value
        # Create a fake 'connect' method that does nothing but record being called
        mock_instance.connect = AsyncMock()
        # Create a fake 'disconnect' method that does nothing but record being called
        mock_instance.disconnect = AsyncMock()
        # Create a fake 'place_order' method that returns a successful response
        mock_instance.place_order = AsyncMock(return_value={"orderId": 999, "status": "FILLED"})
        
        # Create a valid order object to use for the test execution
        order = OrderValidator(symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.002)
        
        # Run the full execution flow that we want to test
        response = await execute_order(order)
        
        # Verify that the response ID matches the fake ID we set up earlier
        assert response["orderId"] == 999
        # Verify that the 'connect' method was called exactly once during the process
        mock_instance.connect.assert_called_once()
        # Verify that 'place_order' was called with the exact order data we provided
        mock_instance.place_order.assert_called_once_with(order)
        # Verify that the 'disconnect' method was called to close the connection properly
        mock_instance.disconnect.assert_called_once()