from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "Pizza Delivery API"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
