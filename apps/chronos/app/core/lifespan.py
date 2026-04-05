"""C.H.R.O.N.O.S. lifespan."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("C.H.R.O.N.O.S. — Tactical Intelligence starting up")
    yield
    logger.info("C.H.R.O.N.O.S. — shutting down")
