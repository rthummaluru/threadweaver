import jwt
from fastapi import HTTPException, Depends, Header
from config import config
from app.db.supabase_client import get_supabase_connection

jwks_client = jwt.PyJWKClient(config.supabase_jwks_url)

def verify_token(token: str) -> dict:
    """
    Verify the token
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=["ES256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user_id(authorization: str = Header(..., description="JWT token")) -> str:
    """
    Get the current user id from the token
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header provided")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]

    payload = verify_token(token)
    return payload["sub"]