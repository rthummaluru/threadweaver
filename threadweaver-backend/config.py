import os 
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    #API configuration
    app_name: str = Field(
        default="Threadweaver", description="The name of the application"
    )
    app_version: str = Field(
        default="1.0.0", description="The version of the application"
    )
    debug: bool = Field(
        default=False, description="Whether to run the application in debug mode"
    )

    # Server configuration
    host: str = Field(
        default="0.0.0.0", description="The host to run the application on"
    )
    port: int = Field(
        default=8000, description="The port to run the application on"
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO", description="The level of logging to run the application on"
    )

    # Database configuration
    supabase_url: Optional[str] = Field(
        default=None, description="The URL of the Supabase database", repr=False
    )
    supabase_key: Optional[str] = Field(
        default=None, description="The API key for the Supabase database", repr=False
    )

    # AI configuration
    openai_api_key: Optional[str] = Field(
        default=None, description="The API key for the OpenAI API", repr=False
    )
    anthropic_api_key: Optional[str] = Field(
        default=None, description="The API key for the Anthropic API", repr=False
    )
    langsmith_api_key: Optional[str] = Field(
        default=None, description="The API key for the LangSmith API", repr=False
    )

    # CORS configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"], description="Allowed CORS origins"
    )

    def get_embedding_model(self, embedding_model: Optional[str] = None, **kwargs) -> any:
        """ Get the embedding model """
        from langchain_openai import OpenAIEmbeddings

        model = embedding_model or "text-embedding-3-small"
        return OpenAIEmbeddings(model=model, **kwargs)

    notion_token: Optional[str] = Field(
        default=None, description="The API key for the Notion API", repr=False
    )

config = Config()



