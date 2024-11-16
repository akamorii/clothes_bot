import aiosqlite
import asyncio

DB_PATH = "./clothes_store.db"

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

async def db_show(row, table):
    async with aiosqlite.connect(DB_PATH) as con:
        cursor = await con.execute(f"SELECT {row} FROM {table}")
        rows = await cursor.fetchall()  # Используем await, так как fetchall асинхронен в aiosqlite
        return rows

async def main():
    await db_start()
    rows = await db_show('collection', 'clothes')
    print(rows)  # выводим результат работы db_show
    # await add_clothes_db('clothes', 'anycollection', 't_shirt', 'green')
    # await db_drop()  # Раскомментируйте, если хотите удалить таблицу

if __name__ == "__main__":
    asyncio.run(main())
