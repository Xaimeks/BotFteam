import asyncpg
import asyncio
import os
from os import getenv
from dotenv import load_dotenv

async def db_main():
    try:
        conn = await asyncpg.connect(user=getenv('DB_USER'),
                                    password=getenv('DB_PASSWORD'),
                                    database=getenv('DB_NAME'),
                                    host=getenv('DB_HOST'))
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных {e}")
    
async def fetch_user_data(user_id: int):
    try:
        conn = await db_main()
        try:
            rows = await conn.fetch('SELECT user_id, username, status, percent, balance, daily_profit, monthly_profit, total_profit, fake_tag FROM user_stats WHERE user_id = $1', user_id)
            return rows
        finally:
            await conn.close()
    except Exception as e:
        print(f"Ошибка извлечения данных о пользователе {e}")
        return None
    finally:
        await conn.close()

async def fetch_withdraw_request(user_id: int):
    try:
        conn = await db_main()
        try:
            rows = await conn.fetch('SELECT id, user_id, amount, status, created_at, updated_at FROM withdraw_request WHERE user_id = $1', user_id)
            return rows
        finally:
            await conn.close()
    except Exception as e:
        print(f"Ошибка извлечения данных о запросах на вывод {e}")
        return None
    finally:
        await conn.close()

async def insert_user_data(user_id: int, username: str):
    conn = await db_main()
    try:
        await conn.execute('''
            INSERT INTO user_stats (user_id, username)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
        ''', user_id, username)
    except Exception as e:
        print(f"Ошибка при добавлении пользователя в дб {e}")
    finally:
        await conn.close()