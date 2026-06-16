from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OSRM_BASE_URL: str = "https://router.project-osrm.org"
    REQUEST_TIMEOUT: int = 20

    class Config:
        env_file = ".env"


settings = Settings()