from pydantic import BaseSettings, Field
class Settings(BaseSettings):
    google_sa_json: str = Field(..., env="GOOGLE_SA_JSON")  # base64
    database_url: str
    tz_offset: int = -7  # PST default
    class Config: env_file = ".env"
settings = Settings()