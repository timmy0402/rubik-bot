import os
from dotenv import load_dotenv
from bot import RubiksBot
import logging


load_dotenv()

if __name__ == "__main__":
    if os.getenv("ENV", "").upper() == "PROD":
        token = os.getenv("TOKEN")
    else:
        token = os.getenv("TEST_TOKEN")

    bot = RubiksBot()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s", level=logging.INFO
    )
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("discord").setLevel(logging.WARNING)
    bot.run(token)
