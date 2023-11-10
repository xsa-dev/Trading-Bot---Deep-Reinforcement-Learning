import os
import dotenv
import yaml

dotenv.load_dotenv("/home/alxy/Codes/Trading-Bot---Deep-Reinforcement-Learning/.env")

SETTINGS_PATH = os.getenv("SETTINGS" or '../config/settings.yaml')

settings_yaml = None
with open(SETTINGS_PATH, "r") as file:
    settings_yaml = yaml.safe_load(file)

class Settings:
    def __init__(self) -> None:
        self.optimisation = True
        self.scope = settings_yaml.get("symbols" or 'BTC/USDT')


settings = Settings()

HOST = os.getenv("DB_HOST" or settings.db.host)
PORT = os.getenv("DB_PORT" or settings.db.port)
NAME = os.getenv("DB_NAME" or settings.db.name)
USER = os.getenv("DB_USER" or settings.db.user)
PASS = os.getenv("DB_PASS" or settings.db.pwd)
SCHEMA = os.getenv("DB_SCHEMA" or settings.db.schema)
