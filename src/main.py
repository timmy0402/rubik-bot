import os
from dotenv import load_dotenv
from bot import RubiksBot
import logging

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    """
    Main entry point for the Rubik Discord Bot.
    Initializes the bot, sets up logging, and runs with the appropriate token.
    """
    # Determine which token to use based on the environment
    if os.getenv("ENV", "").upper() == "PROD":
        token = os.getenv("TOKEN")
    else:
        token = os.getenv("TEST_TOKEN")

    # Initialize the bot instance
    bot = RubiksBot()

    # Configure logging to display timestamps, levels, and source names
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s", level=logging.INFO
    )

    # Set external libraries' logging levels to WARNING to reduce noise in logs
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("discord").setLevel(logging.WARNING)

    # Start the bot
    bot.run(token)