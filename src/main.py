import os
from dotenv import load_dotenv
from bot import RubiksBot

load_dotenv()

if __name__ == "__main__":
    if os.getenv("ENV", "").upper() == "PROD":
        token = os.getenv("TOKEN")
    else:
        token = os.getenv("TEST_TOKEN")

    bot = RubiksBot()
    bot.run(token)
