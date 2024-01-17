import aiosqlite
from typing import Union


class Query:
    def __init__(self):
        self.sqlpath = 'ttele.db'

    async def execute_query(self, query, values=None, commit=True):
        async with aiosqlite.connect(self.sqlpath, uri=True) as db:
            cursor = await db.cursor()
            try:
                if values is not None:
                    await cursor.execute(query, values)
                else:
                    await cursor.execute(query)
                if commit:
                    await db.commit()
                    return None
                else:
                    rows = await cursor.fetchall()
                    return rows
            except Exception as e:
                await db.rollback()
                raise e

    async def create_data(self, table_name: str, fields: list, values: Union[list, str]):
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
        await self.execute_query(query, values)

    async def read_data(self, table_name: str, fields: list = None, condition: str = None, condition_values: Union[list, str] = None):
        query = f"SELECT {', '.join(fields) if fields else '*'} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return await self.execute_query(query, condition_values, commit=False)

    async def update_data(self, table_name: str, fields: list, values: Union[list, str], condition: str = None, condition_values: Union[list, str] = None):
        set_values = ', '.join([f"{field} = ?" for field in fields])
        query = f"UPDATE {table_name} SET {set_values}"
        if condition:
            query += f" WHERE {condition}"
        await self.execute_query(query, values + condition_values if condition_values else values)

    async def delete_data(self, table_name: str, condition: str = None, condition_values: Union[list, str] = None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        await self.execute_query(query, condition_values)


