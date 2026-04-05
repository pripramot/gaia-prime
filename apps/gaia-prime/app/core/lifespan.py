"""Application lifespan — startup / shutdown hooks."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.db import db_manager
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("GAIA PRIME — Ring-Forge starting up")
    await db_manager.connect()
    await db_manager.initialize_schema()
    yield
    logger.info("GAIA PRIME — shutting down")
    await db_manager.disconnect()
