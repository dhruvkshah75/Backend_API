from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. Database (Unified URL)
    # This will read 'DATABASE_URL' from Docker or your .env file
    database_url: str

    # 2. Security / JWT
    # These automatically map to SECRET_KEY, ALGORITHM, etc.
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",       # Ignores extra variables in .env
        case_sensitive=False  # Allows matching 'database_url' to 'DATABASE_URL'
    )

settings = Settings()