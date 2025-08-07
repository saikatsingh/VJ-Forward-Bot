# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from pyrogram import Client as VJ, filters, idle
from pyrogram import Client as UserClient

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("forward_bot.log", maxBytes=5000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Bot Client (for handling commands) ---
VJBot = VJ(
    "VJ-Forward-Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=120,
    plugins=dict(root="plugins")
)

# --- User Client (String session for forwarding) ---
User = UserClient(
    name="forward-user",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.STRING_SESSION
)

# --- Source/Destination Configuration ---
SOURCE_CHANNEL_ID = Config.SOURCE_CHANNEL_ID      # example: -100123456789
DESTINATION_CHANNEL_ID = Config.DEST_CHANNEL_ID   # example: -100987654321

# --- Real-time Forwarding Logic ---
@User.on_message(filters.chat(SOURCE_CHANNEL_ID))
async def forward_to_destination(client, message):
    try:
        await message.forward(DESTINATION_CHANNEL_ID)
        logger.info(f"Forwarded message {message.id} to destination.")
    except Exception as e:
        logger.error(f"Error forwarding message: {e}")

# --- Main Runner ---
async def main():
    await VJBot.start()
    await User.start()
    logger.info("VJ Forward Bot is up and running!")
    await idle()
    await VJBot.stop()
    await User.stop()

if __name__ == "__main__":
    asyncio.run(main())
