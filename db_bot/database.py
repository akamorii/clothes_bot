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


async def add_order_to_db(sized_item, user_id, addr, status='unknown', tracknum='unknown'):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(
            """
            INSERT INTO orders (sized_item, user_id, addr, status, tracknum)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sized_item, user_id, addr, status, tracknum),
        )
        await con.commit()
 
 
async def count_update_db(operation, uptable_count, id):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"UPDATE sizes_and_counts SET count = count {operation} {uptable_count} WHERE sized_item_id == {id}")
        await con.commit()
        
        
async def order_update_db(table = 'orders',column = 'status', mean = 'собираем', id_name = 'order_id', id = 1):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"UPDATE {table} SET {column}='{mean}' WHERE {id_name} == {id}")
        await con.commit()
        

async def db_drop(table) -> None:
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"DROP TABLE IF EXISTS {table}")
        await con.commit()


async def delete_item_from_db(table = 'clothes',collection = None, color = None):
    async with aiosqlite.connect(DB_PATH) as con:
        await con.execute(f"DELETE FROM {table} WHERE collection == '{collection}' AND color == '{color}'")
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
        return (rows)



async def select_ids_from_db (id, table, eq1, eq2, eq3 = 1, eq4 = 1) -> list:
    """
    получить id двух элементов
    
    :param table: Имя таблицы.
    :param id: имя элемента который мы хотим получить.
    """
    query = f"SELECT {id} FROM {table}  WHERE {eq1} == '{eq2}' AND {eq3} == '{eq4}'"

    async with aiosqlite.connect(DB_PATH) as con:
        cursor = await con.execute(query)
        rows = await cursor.fetchall()
        return (rows)
    

async def main():
    await db_start()
    # await add_clothes_db('clothes', 'classic', 't_shirt', 'red')
    # rows = await db_show(['collection', 'item'], 'clothes')
    # rows = await select_row_from_db('sizes_and_counts', 'size', '52', 'item_id', '1')
    # rows = await select_ids_from_db('id', 'clothes', 'color', 'white', 'collection', 'classic')
    # rows = await select_row_from_db('orders', 'user_id', 1135754644)
    await order_update_db()
    # print(rows)  # выводим результат работы db_show
    # await count_update_db('-', 1, 1)
    # await db_drop()  # Раскомментируйте, если хотите удалить таблицу

if __name__ == "__main__":
    asyncio.run(main())
