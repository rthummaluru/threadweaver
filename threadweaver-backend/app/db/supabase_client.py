import os
import logging
from typing import Optional
from supabase import create_client, Client
from config import config

logger = logging.getLogger(__name__)

class SupabaseClient:
    """
    Supabase client class
    """
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize the Supabase client
        """
        self.client: Client | None = None

    def connect_to_supabase(self):
        """
        Connect to the Supabase database

        Returns:
            Client: The Supabase client instance

        Raises:
            Exception: If the connection to the Supabase database fails
        """
        try:
            logger.info(f"Connecting to Supabase: {config.supabase_url}")
            self.client = create_client(config.supabase_url, config.supabase_key)
        except Exception as e:
            logger.error(f"Error connecting to Supabase: {e}")
            raise e

    def get_supabase_client(self) -> Client:
        """
        Get the Supabase client instance

        Returns:
            Client: The Supabase client instance

        Raises:
            Exception: If the Supabase client is not initialized
        """
        if not self.client:
            self.connect_to_supabase()
        return self.client
    
    def test_connection(self):
        """
        Test the connection to the Supabase database

        Returns:
            bool: True if the connection is successful, False otherwise

        Raises:
            Exception: If the connection to the Supabase database fails
        """
        try:
            self.client.table("users").select("*").execute()
            logger.info("Connection to Supabase successful")
            return True
        except Exception as e:
            logger.error(f"Error testing connection to Supabase: {e}")
            return False
    
supabase_client = SupabaseClient()

def get_supabase_connection() -> Client:
    """ Get Supabase client instance """
    try:
        logger.info("Connection to Supabase Client")
        return supabase_client.get_supabase_client()
        logger.info("Supabase Client connected successfully")
    except Exception as e:
        logger.error(f"Error getting Supabase client: {e}")
        raise e