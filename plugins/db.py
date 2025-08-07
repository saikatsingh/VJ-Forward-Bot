# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import motor.motor_asyncio
from config import Config

class MongoDB:
    def __init__(self, uri, db_name, collection):
        self.uri = uri
        self.db_name = db_name
        self.collection = collection 
        self.client = None
        self.db = None
        self.files = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        self.files = self.db[self.collection]

    async def close(self):
        if self.client:
            self.client.close()

    async def add_file(self, file_id):
        file = {"file_id": file_id}
        return await self.files.insert_one(file)
        
    async def is_file_exit(self, file_id):
        f = await self.files.find_one({"file_id": file_id})
        return bool(f)
        
    async def get_all_files(self):
        return self.files.find({})
        
    async def drop_all(self):
        return await self.files.drop()


# ✅ New utility to get all forward records
async def get_all_forward_data(uri):
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client[Config.DATABASE_NAME]
    forward_collection = db["FORWARD"]
    return await forward_collection.find({}).to_list(length=1000)


# ✅ Reuse connection logic
async def connect_user_db(user_id, uri, chat):
    chat = f"{user_id}{chat}"
    dbname = f"{user_id}-Forward-Bot"
    db = MongoDB(uri, dbname, chat)
    try:
        await db.connect()
    except Exception as e:
        print(e)
        return False, db
    return True, db
