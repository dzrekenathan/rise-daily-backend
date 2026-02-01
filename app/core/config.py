from pydantic_settings import BaseSettings
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from dotenv import load_dotenv


load_dotenv()


# Configure logging

def configure_logging():
    os.makedirs("./logs", exist_ok=True)

    handler = TimedRotatingFileHandler(
        filename="./logs/risedaily.log",
        when="midnight",
        interval=1,
        backupCount=7
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    # Console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    detailed_handler = TimedRotatingFileHandler(
        filename="./logs/risedaily_detailed.log",
        when="midnight",
        interval=1,
        backupCount=7
    )
    detailed_handler.setFormatter(formatter)
    detailed_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(detailed_handler)


class Settings(BaseSettings):
    APP_NAME: str = "Rise Daily"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")



settings = Settings()
configure_logging()