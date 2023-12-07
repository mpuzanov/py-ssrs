import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from ssrs.logger import get_logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    APP_NAME: str = "ssrs"

    SSRS_BASE_URL: str = '0.0.0.0'
    SSRS_USER: str
    SSRS_PASS: str

    LOG_FILE: str = APP_NAME + '.log'
    LOG_LEVEL: str = 'DEBUG'

    MODE: str

    mail_server: str
    mail_port: int
    mail_use_tls: bool
    mail_use_ssl: bool
    mail_username: str
    mail_password: str
    mail_timeout: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
logger = get_logger(__name__, settings.LOG_LEVEL, settings.LOG_FILE)
