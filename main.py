# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import Config
from plugins.db import get_all_forward_data
from plugins import temp

api_id = Config.API_ID
api_hash = Config.API_HASH
string_session = Config.BOT_SESSION

userbot = Client(name="userbot", api_id=api_id, api_hash=api_hash, session_string=string_session)

@userbot.on_message(filters.text | filters.media)
async def forward_handler(client, message: Message):
    try:
        all_data = await get_all_forward_data(Config.DATABASE_URI)
        for record in all_data:
            source = int(record.get("source", 0))
            destination = int(record.get("destination", 0))
            if message.chat.id == source:
                await message.copy(destination)
                temp.forwardings += 1
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Error in forwarding: {e}")

if __name__ == "__main__":
    print("Bot is running...")
    userbot.run()
