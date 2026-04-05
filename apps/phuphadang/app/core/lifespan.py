"""Phuphadang lifespan."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Phuphadang — Core AI & Digital Forensics starting up")
    yield
    logger.info("Phuphadang — shutting down")
