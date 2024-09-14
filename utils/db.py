import logging
import pathlib
from typing import Optional, Any, Tuple

import aiosqlite

log = logging.getLogger(__name__)

class Database():
    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path

    async def create_tables(self):
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS guilds (
                id TEXT PRIMARY KEY,
                name TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT
            );
            """,
        ]
        
        con = await self.connect()
        cur = await con.cursor()

        for statement in sql_statements:
            await cur.execute(statement)

        await con.commit()
        await cur.close()
        await con.close()


    @staticmethod
    async def _fetch(cursor: aiosqlite.Cursor, mode: str):
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def connect(self) -> aiosqlite.Connection:
        return await aiosqlite.connect(self.db_path)

    async def execute(self, query: str, values: Tuple = (), fetch: str = None, commit: bool = False) -> Optional[Any]:
        """
        :param query: SQL query.
        :param values: values to be passed to the query.
        :param fetch: Takes ('one', 'many', 'all').
        :param commit: Commits the changes to the database if it's set to `True`.
        :return data
        """

        con = await self.connect()
        cur = await con.cursor()

        await cur.execute(query, values)

        if fetch:
            data = await self._fetch(cur, fetch)
        else:
            data = None

        if commit:
            await con.commit()

        await cur.close()
        await con.close()

        return data

    async def run(self, query: str, values: Tuple = ()) -> None:
        """
        runs the query and commits any changes to the database directly.

        :param query: SQL query
        :param values: values to be passed to the query.
        """

        await self.execute(query, values, commit=True)
