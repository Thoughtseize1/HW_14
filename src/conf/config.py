from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'default'
    secret_key: str = 'default'
    domain: str = 'default'
    algorithm: str = 'default'
    mail_username: str = 'your-email@example.com'
    mail_password: str = 'default'
    mail_from: str = 'your-email@example.com'
    mail_port: int = 123
    mail_server: str = 'default'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    # model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8', extra='ignore')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
