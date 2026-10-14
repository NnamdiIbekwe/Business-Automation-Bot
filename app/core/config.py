from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

app_name: str = "Business Automation Bot"
database_url: str = ""
api_key: str = ""
allowed_webhook_hosts: List[str] = []
scheduler_interval_seconds: int = 0
webhook_timeout_seconds: float = 10.0

@lru_cache()
def get_settings() -> Settings:
    return Settings()