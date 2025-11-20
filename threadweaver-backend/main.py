from typing import Union
from fastapi import FastAPI
import logging
import uvicorn
from config import config
from fastapi.middleware.cors import CORSMiddleware
from app.db.supabase_client import get_supabase_connection, supabase_client
from app.api.chat import router as chat_router
from app.api.users import router as users_router
from app.api.sessions import router as sessions_router
import supabase

# Create the FastAPI app
app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    debug=config.debug
)


# Configure logging
logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to {config.app_name} {config.app_version}!"}

@app.get('/health')
async def health_check():
    return {
        "status": "healthy",
        "app_name": config.app_name,
        "app_version": config.app_version,
    }

@app.on_event("startup")
async def startup_event():
    """ Startup event """
    logger.info("Starting up...")
    try:
        # Initialize the Supabase client connection
        supabase_client.connect_to_supabase()
        
        # Test the connection
        if not supabase_client.test_connection():
            raise Exception("Failed to connect to Supabase")
        logger.info("Supabase connected successfully")
    except Exception as e:
        logger.error(f"Error starting up: {e}")
        raise e

app.include_router(chat_router)
app.include_router(users_router)
app.include_router(sessions_router)
if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)