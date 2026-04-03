"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter
from loguru import logger

from src.services.db_service import DatabaseService

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Check application and database health."""
    try:
        db_service = DatabaseService()
        health = await db_service.health_check()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": health,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
        }
