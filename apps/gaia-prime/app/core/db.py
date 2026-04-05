"""Database manager instance for GAIA PRIME."""
from app.core.settings import get_app_settings
from gaia_shared.database import DatabaseManager

_settings = get_app_settings()


# Extend base manager with schema initialization
class GaiaDatabaseManager(DatabaseManager):
    async def initialize_schema(self) -> None:
        async with self.transaction():
            await self.execute(
                """
                CREATE TABLE IF NOT EXISTS data_records (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    source      TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    payload     TEXT NOT NULL,
                    checksum    TEXT NOT NULL,
                    status      TEXT NOT NULL DEFAULT 'raw',
                    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed_at DATETIME
                )
                """
            )
            await self.execute(
                """
                CREATE TABLE IF NOT EXISTS processing_jobs (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id      TEXT UNIQUE NOT NULL,
                    pipeline    TEXT NOT NULL,
                    status      TEXT NOT NULL DEFAULT 'pending',
                    records_in  INTEGER DEFAULT 0,
                    records_out INTEGER DEFAULT 0,
                    error       TEXT,
                    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                    finished_at DATETIME
                )
                """
            )


db_manager = GaiaDatabaseManager(_settings.database_url)
