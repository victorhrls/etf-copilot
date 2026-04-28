from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    fred_api_key: str
    raw_data_path: Path = Path("data/raw")
    features_path: Path = Path("data/features")

    class Config:
        env_file = ".env"


settings = Settings()