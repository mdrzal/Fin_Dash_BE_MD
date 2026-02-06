
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import general
from app.services.logging_service import LoggingService
from app.startup.vader_startup import init_vader_sia
from app.scripts.init_stocks_db import initiate_db as init_stocks_db_main
from app.db import get_db_connection

logger = LoggingService.get_logger(__name__)

# --- startup code ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application")
    try:
        init_stocks_db_main()
        logger.info("database initialized.")
    except Exception as e:
        logger.exception(f"Failed to initialize database: {e}")
    
    try:
        init_vader_sia()
        logger.info("VADER sentiment analyzer loaded")
    except Exception as e:
        logger.exception(f"Failed to initialize VADER: {e}")
    # Register DB connection
    app.state.db_connection = get_db_connection()
    yield
    logger.info("Shutting down FastAPI application")

app = FastAPI(
    title="Financial Analysis Backend",
    description="API for financial data and analysis.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(general.router, prefix="", tags=["General"])