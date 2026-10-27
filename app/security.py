from fastapi import Header, HTTPException, status
import secrets

def require_api_key(x_api_key: str = Header(default="")) -> None:
    expected = get_settings().api_key.encode()
    if not secrets.compare_digest(x_api_key.encode(), expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing X_API_KEY")