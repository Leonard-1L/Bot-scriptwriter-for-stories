import os

from dotenv import load_dotenv

GPT_URL = "http://localhost:1234/v1/chat/completions"  # http://127.0.0.1:8000/v1/chat/completions Путь к серверу нейросети

LOGS_PATH = "logs.txt"  # Путь к файлу логов

MODEL_NAME = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"  # Название используемой нейросети

MAX_MODEL_TOKENS = 128  # Максимальный размер ответа

DB_NAME = "db.sqlite"  # Название базы данных

DB_TABLE_USERS_NAME = "users"  # Название таблицы пользователей в базе

ADMINS = [12345]  # Список user_id админов

MAX_SESSIONS = 39  # Максимальное количество сессий на пользователя

MAX_TOKENS_PER_SESSION = 1000  # Максимальное количество токенов на сессию

MAX_USERS = 3  # Максимальное количество пользователей приложения

load_dotenv()

FOLDER_ID = os.getenv("FOLDER_ID")
IAM_TOKEN = os.getenv("IAM_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
