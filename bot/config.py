# Import os to read environment variables from the operating system
import os
# Import Path to find files on the computer regardless of the operating system
from pathlib import Path
# Import load_dotenv to pull variables from a text file into the script
from dotenv import load_dotenv
# Import BaseSettings to make a class that automatically validates settings
from pydantic_settings import BaseSettings, SettingsConfigDict

# Find the .env file in the current folder where the script is running
env_path = Path(".") / ".env"
# Read the .env file so the variables are available to the script
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # This class centralizes all the settings for the trading bot
    
    # Read the Binance API Key from the loaded environment variables
    API_KEY: str = os.getenv("BINANCE_API_KEY")
    # Read the Binance API Secret from the loaded environment variables
    API_SECRET: str = os.getenv("BINANCE_API_SECRET")
    
    # The base URL for the Binance Futures Testnet environment
    BASE_URL: str = "https://testnet.binancefuture.com"
    # Boolean flag to tell the Binance library we are using the testnet
    TESTNET: bool = True
    
    # The file path where all the trading logs will be saved
    LOG_FILE: str = "logs/trading_bot.log"
    
    # Pydantic configuration to manage how variables are loaded
    model_config = SettingsConfigDict(
        # Tell the class to look at the .env file specifically
        env_file=".env", 
        # Skip any extra variables in the .env that are not defined here
        extra="ignore"
    )

# Create a single instance of settings to use in other files
settings = Settings()