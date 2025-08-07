# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from pyrogram import Client as VJ, filters, idle
from pyrogram import Client as UserClient
from plugins.db import get_all_forward_data  # 👈 your DB function

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

# --- Bot Client ---
VJBot = VJ(
    "VJ-Forward-Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=120,
    plugins=dict(root="plugins")
)

# --- UserBot Client ---
User = UserClient(
    name="forward-user",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.STRING_SESSION
)

# --- Real-time forwarding handler builder ---
async def setup_forward_handlers():
    all_data = get_all_forward_data()  # 👈 should return a list of dicts with source & dest

    if not all_data:
        logger.warning("No source-destination mappings found in database.")
        return

    for item in all_data:
        source_id = item.get("source_chat_id")
        dest_id = item.get("destination_chat_id")

        if not source_id or not dest_id:
            continue

        logger.info(f"Setting up forwarder: {source_id} ➜ {dest_id}")

        @User.on_message(filters.chat(source_id))
        async def forward_new_message(client, message, dest=dest_id):
            try:
                await message.forward(dest)
                logger.info(f"Forwarded message from {source_id} to {dest}")
            except Exception as e:
                logger.error(f"Error forwarding from {source_id} to {dest_id}: {e}")

# --- Main Runner ---
async def main():
    await VJBot.start()
    await User.start()
    await setup_forward_handlers()
    logger.info("VJ Forward Bot is up and running with real-time forwarding!")
    await idle()
    await VJBot.stop()
    await User.stop()

if __name__ == "__main__":
    asyncio.run(main())
