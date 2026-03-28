# Import the sys module to handle system-level outputs like the terminal
import sys
# Import the os module to create folders and check if files exist
import os
# Import the logger from the loguru library for structured logging
from loguru import logger

def setup_logger():
    # This function configures how the bot records its activity
    
    # Check if the folder named logs exists in the current directory
    if not os.path.exists("logs"):
        # Create the logs folder if it is missing
        os.makedirs("logs")

    # Remove the default loguru settings to start with a clean configuration
    logger.remove()

    # Configure the terminal output (sys.stderr)
    logger.add(
        # Send logs to the standard error output of the terminal
        sys.stderr, 
        # Define the message format with timestamp, level, and the message text
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", 
        # Enable colors to make logs easier to read in the terminal
        colorize=True
    )

    # Configure the file output
    logger.add(
        # Save all logs to a file inside the logs folder
        "logs/trading_bot.log", 
        # Define the text format for the file (no colors allowed in text files)
        format="{time} | {level} | {message}"
    )
    
    # Return the configured logger instance
    return logger

# Create a single global log instance to be used by all other files
log = setup_logger()