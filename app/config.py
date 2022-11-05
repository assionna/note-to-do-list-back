from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    # db_url: str = 'postgresql://username:password@localhost:5432/database'


settings = Settings()
