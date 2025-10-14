from typing import Union
from fastapi import FastAPI
import logging
from config import config

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    debug=config.debug
)


logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

