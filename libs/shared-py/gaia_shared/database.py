"""Shared database manager for GAIA PRIME services."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import aiosqlite


class DatabaseManager:
    """Async database manager supporting SQLite and PostgreSQL."""

    def __init__(self, database_url: str):
        self._url = database_url
        self._sqlite_conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> None:
        if self._url.startswith("sqlite"):
            db_path = self._url.replace("sqlite:///", "")
            self._sqlite_conn = await aiosqlite.connect(db_path)
            self._sqlite_conn.row_factory = aiosqlite.Row

    async def disconnect(self) -> None:
        if self._sqlite_conn:
            await self._sqlite_conn.close()
            self._sqlite_conn = None

    async def execute(self, query: str, parameters: tuple = ()) -> aiosqlite.Cursor:
        if self._sqlite_conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return await self._sqlite_conn.execute(query, parameters)

    async def fetchall(self, query: str, parameters: tuple = ()) -> list:
        cursor = await self.execute(query, parameters)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def fetchone(self, query: str, parameters: tuple = ()) -> Optional[dict]:
        cursor = await self.execute(query, parameters)
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def commit(self) -> None:
        if self._sqlite_conn:
            await self._sqlite_conn.commit()

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        try:
            yield
            await self.commit()
        except Exception:
            if self._sqlite_conn:
                await self._sqlite_conn.rollback()
            raise
