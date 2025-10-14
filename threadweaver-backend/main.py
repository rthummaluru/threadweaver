from typing import Union
from fastapi import FastAPI
import logging
from config import config
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)