from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import time
import sys
import os

# Add stubs to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import auth, user_management
from app.config import settings
from utils.logging import setup_logging, get_logger, log_request
from utils.master_admin_setup import initialize_master_admin_if_needed
from db.db_config import create_tables

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    logger.info("🚀 Starting User Management System API")
    
    try:
        # Initialize database tables
        create_tables()
        logger.info("✅ Database tables initialized")
        
        # Initialize Master Admin if needed
        initialize_master_admin_if_needed()
        logger.info("✅ Master Admin initialization completed")
        
        logger.info("🎯 User Management System API is ready!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {e}")
        raise
    
    yield
    
    # Shutdown procedures
    logger.info("🛑 Shutting down User Management System API")

app = FastAPI(
    title="User Management System API",
    description="Role-based user management system with Master Admin, Regular Admin, and Employee accounts",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_request(
        logger=logger,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=process_time
    )
    
    return response

# Security middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure this properly for production
    )

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user_management.router)

@app.get("/")
async def root():
    return {
        "message": "User Management System API Running",
        "version": "1.0.0",
        "features": [
            "Master Admin Account Management",
            "Regular Admin Account Creation",
            "Employee Account Management",
            "Role-based Access Control",
            "JWT Authentication",
            "Secure Password Hashing"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-management-system"}