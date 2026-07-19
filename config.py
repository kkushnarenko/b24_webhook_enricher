import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / '.env'

#Ручной парсинг файла .env
if dotenv_path.exists():
    with open(dotenv_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")


BITRIX24_WEBHOOK_URL=os.getenv("BITRIX24_WEBHOOK_URL")
BITRIX_USER_FIELD=os.getenv("BITRIX_USER_FIELD")
CURRENCY_API_URL=os.getenv("CURRENCY_API_URL")

if not BITRIX24_WEBHOOK_URL:
    raise ValueError("BITRIX24_WEBHOOK_URL не настроен в .env")

