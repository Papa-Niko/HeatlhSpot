from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URL from environment variable
MONGO_URL = os.getenv("MONGODB_URI", "mongodb+srv://rohitsetia2005:setia76448@cluster0.5pxqz2u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

try:
    # Connect to MongoDB with error handling
    client = AsyncIOMotorClient(MONGO_URL)
    # Ping the database to validate connection
    client.admin.command('ping')
    logging.info("Successfully connected to MongoDB")
    
    # Get database instance
    db = client["mydb"]  # Database name can also be moved to env variable
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise
