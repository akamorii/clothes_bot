import aiosqlite
import asyncio

DB_PATH = "db_bot/clothes_store.db"

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
        await con.execute("""
            CREATE TABLE IF NOT EXISTS sizes_and_counts(
                sized_item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                size INTEGER NOT NULL,
                count INTEGER,
                item_id INTEGER NOT NULL,
                FOREIGN KEY (item_id) REFERENCES clothes (id)
            )
        """)
        await con.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                sized_item INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                addr TEXT NOT NULL,
                status INTEGER,
                tracknum INTEGER,
                FOREIGN KEY (sized_item) REFERENCES sizes_and_counts (sized_item_id)
            )
        """)
        await con.commit()
        

async def add_clothes_db(table, collection, item_name, color):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"INSERT INTO {table} (collection, item, color) VALUES (?, ?, ?)", 
                          (collection, item_name, color))
        await con.commit()


async def db_drop(table) -> None:
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"DROP TABLE IF EXISTS {table}")
        await con.commit()


async def db_show(columns, table, eq1=1): 
    """
    Получить данные из таблицы с указанными колонками.
    
    :param columns: Список полей для выборки.
    :param table: Имя таблицы.
    :return: Список строк с результатами выборки.
    """
    # Проверяем и подготавливаем колонки для выборки
    if not columns or not isinstance(columns, (list, tuple)):
        raise ValueError("columns должны быть списком или кортежем строк.")

    # Объединяем имена колонок через запятую
    columns_str = ", ".join(f'"{col}"' for col in columns)  # Экранируем названия колонок
    
    # SQL запрос с безопасным подставлением названий колонок и таблицы
    query = f"SELECT {columns_str} FROM {table} WHERE {eq1} > 0"

    async with aiosqlite.connect(DB_PATH) as con:
        cursor = await con.execute(query)
        rows = await cursor.fetchall()  # Получаем все строки
        return rows
    
    
async def select_row_from_db (table, eq1, eq2, eq3 = 1, eq4 = 1) -> list:
    """
    получить строчку из базы данных
    
    :param table: Имя таблицы.
    """
    query = f"SELECT * FROM {table} WHERE {eq1} == {eq2} AND {eq3} == {eq4}"

    async with aiosqlite.connect(DB_PATH) as con:
        cursor = await con.execute(query)
        rows = await cursor.fetchall()
        return (rows[0])

async def main():
    await db_start()
    # await add_clothes_db('clothes', 'classic', 't_shirt', 'red')
    # rows = await db_show(['collection', 'item'], 'clothes')
    rows = await select_row_from_db('sizes_and_counts', 'size', '52', 'item_id', '1')
    print(rows)  # выводим результат работы db_show
    # await db_drop()  # Раскомментируйте, если хотите удалить таблицу

if __name__ == "__main__":
    asyncio.run(main())
