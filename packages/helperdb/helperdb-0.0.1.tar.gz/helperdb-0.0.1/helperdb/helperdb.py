import aiosqlite

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def path(self, path):
        self.db_path = path
        
    async def connect(self):
        self.db = await aiosqlite.connect(self.db_path)
        self.db.row_factory = aiosqlite.Row

    async def close(self):
        await self.db.close()

    async def execute(self, query, *args):
        await self.db.execute(query, *args)
        await self.db.commit()

    async def fetch(self, query, *args):
        cursor = await self.db.execute(query, *args)
        return await cursor.fetchall()
    
    async def fetchone(self, query, *args):
        cursor = await self.db.execute(query, *args)
        return await cursor.fetchone()
