from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    backend_api_url: str
    redis_host: str
    redis_port: int
    redis_db: int


    class Config:
        env_file = ".env"


settings = Settings()