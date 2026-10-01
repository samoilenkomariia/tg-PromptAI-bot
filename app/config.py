import os

from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Не заповнена конфігурація {name}")
    return value

BOT_TOKEN = required("BOT_TOKEN")
GROQ_API_KEY = required("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
RUN_MODE = os.getenv("RUN_MODE", "polling").strip().lower()
PORT = int(os.getenv("PORT", "10000"))
WEBHOOK_BASE_URL = os.getenv(
    "WEBHOOK_BASE_URL", ""
).strip().rstrip("/")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()

STUDENT_NAME = os.getenv("STUDENT_NAME", "Не вказано")
STUDENT_GROUP = os.getenv("STUDENT_GROUP", "Не вказано")
CONTACT_PHONE = os.getenv("CONTACT_PHONE", "Не вказано")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "Не вказано")