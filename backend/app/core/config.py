from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # Comma-separated list of front-end origins allowed to call the API.
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    # VIP seats cost this many times the session's base price.
    VIP_PRICE_MULTIPLIER: float = 2.0

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
