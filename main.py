#
import os
import logging
import traceback
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import db  # Import database connection
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="HealthSpot API",
    description="Backend API for HealthSpot application",
    version="1.0.0",
)

# Configure CORS based on environment
DEFAULT_ORIGINS = [
    "http://localhost:3000",  # React development
    "http://127.0.0.1:5500",  # Live Server
]

# Get production origins from environment variable
PRODUCTION_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://myhealthspot.netlify.app")
origins = DEFAULT_ORIGINS + PRODUCTION_ORIGINS.split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

# Error handler middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )

# API Endpoints
@app.post("/add-user")
async def add_user(user: User):
    try:
        logger.info(f"Adding new user: {user.email}")
        result = await db["users"].insert_one(user.dict())
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error adding user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add user: {str(e)}")

@app.get("/get-users")
async def get_users():
    try:
        logger.info("Retrieving all users")
        users = await db["users"].find().to_list(100)
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
            
        result = await db["users"].delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {"deleted_count": result.deleted_count}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "HealthSpot API is running"}

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting HealthSpot API")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down HealthSpot API")
