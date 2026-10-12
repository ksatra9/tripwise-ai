import sys
from pathlib import Path

# Ensure project root is in sys.path so 'backend' can be imported when run directly
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.seed_data import seed_database
from backend.app.routers import plan, destinations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("tripwise.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and demo seed data is loaded
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        seed_database(db)
        db.close()
    except Exception as e:
        logger.warning(f"Seed database initialization check: {e}")
    yield
    # Shutdown
    logger.info("Application shutting down.")

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Personalized Travel Itinerary Recommendation System for travel in India. "
        "Transforms natural language trip descriptions into mathematically verified, "
        "strictly affordable day-by-day itineraries with honest cost breakdowns."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plan.router)
app.include_router(destinations.router)

@app.get("/api/health", tags=["System"])
def health_check():
    """Health check endpoint reporting system status and model configuration."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "gemini_model": settings.GEMINI_MODEL,
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
