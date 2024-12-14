import os

class Config:
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    ENV = os.environ.get("ENV", "development")

    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///game.db")
    
    MARKET_REFRESH_INTERVAL = int(os.environ.get("MARKET_REFRESH_INTERVAL", 5))

if Config.ENV == "production" and (not Config.SECRET_KEY or not Config.DATABASE_URL):
    raise ValueError("SECRET_KEY and DATABASE_URL must be set in prod.")

config = Config()