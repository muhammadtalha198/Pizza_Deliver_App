from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "Pizza Delivery API"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # access token info
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    # email verification
    SENDGRID_API_KEY: str
    EMAIL_SENDER: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
