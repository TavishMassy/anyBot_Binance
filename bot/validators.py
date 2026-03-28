# Import the main Pydantic class to create data models
from pydantic import BaseModel, Field, model_validator
# Import typing tools to define optional fields and specific string choices
from typing import Optional, Literal

class OrderValidator(BaseModel):
    # This class checks that all user input is correct before the bot uses it
    
    # Symbol must be a string that follows a specific naming pattern for trading pairs
    symbol: str = Field(..., pattern=r"^[A-Z0-9]{5,15}$")
    # Side must be exactly 'BUY' or 'SELL'
    side: Literal["BUY", "SELL"]
    # Order type must be one of these three specific categories
    order_type: Literal["LIMIT", "MARKET", "STOP_MARKET"]
    # Quantity must be a number greater than zero
    quantity: float = Field(..., gt=0)
    # Price is not required for all orders so it is optional and defaults to None
    price: Optional[float] = None
    # Stop price is not required for all orders so it is optional and defaults to None
    stop_price: Optional[float] = None

    @model_validator(mode='after')
    def check_required_prices(self) -> 'OrderValidator':
        # This function runs after the basic field checks to look for missing data
        
        # If the user chose a LIMIT order, they must provide a price
        if self.order_type == "LIMIT" and self.price is None:
            # Raise an error if the price is missing for a LIMIT trade
            raise ValueError("Price is mandatory for LIMIT orders.")
            
        # If the user chose a STOP_MARKET order, they must provide a stop price
        if self.order_type == "STOP_MARKET" and self.stop_price is None:
            # Raise an error if the stop price is missing for a STOP_MARKET trade
            raise ValueError("Stop Price is mandatory for STOP_MARKET orders.")
            
        # Return the validated object if all checks pass
        return self