# Import the pytest library to handle automated testing
import pytest
# Import the specific error that Pydantic throws when data fails validation
from pydantic import ValidationError
# Import the validator class that defines our order rules
from bot.validators import OrderValidator

def test_limit_order_missing_price():
    # This function tests that the bot blocks a LIMIT order if no price is provided
    
    # We tell the test to expect a ValidationError to happen inside this block
    # We also look for the specific error message "Price is mandatory"
    with pytest.raises(ValidationError, match="Price is mandatory"):
        # We try to build a LIMIT order object but deliberately forget the price
        OrderValidator(
            symbol="BTCUSDT", side="BUY", order_type="LIMIT", quantity=0.005
        )

def test_stop_market_missing_trigger():
    # This function tests that the bot blocks a STOP_MARKET order if no stop price is provided
    
    # We tell the test to expect a ValidationError to happen inside this block
    # We also look for the specific error message "Stop Price is mandatory"
    with pytest.raises(ValidationError, match="Stop Price is mandatory"):
        # We try to build a STOP_MARKET order object but leave out the stop_price field
        OrderValidator(
            symbol="BTCUSDT", side="BUY", order_type="STOP_MARKET", quantity=0.005
        )