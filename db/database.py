import aiosqlite
import asyncio

DB_PATH = "db/clothes_store.db"

async def db_start():
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute("""
            CREATE TABLE IF NOT EXISTS clothes(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                collection TEXT DEFAULT 'classic',
                item TEXT NOT NULL,
                color TEXT NOT NULL
            )
        """)
        await con.commit()

async def add_clothes_db(table, collection, item_name, color):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"INSERT INTO {table} (collection, item, color) VALUES (?, ?, ?)", 
                          (collection, item_name, color))
        await con.commit()

async def db_drop():
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute("DROP TABLE IF EXISTS clothes")
        await con.commit()

async def main():
    await db_start()
    await add_clothes_db('clothes', 'classic', 't_shirt', 'white')
    # await db_drop()  # Раскомментируйте, если хотите удалить таблицу

if __name__ == "__main__":
    asyncio.run(main())
