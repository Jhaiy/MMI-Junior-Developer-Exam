import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 3)) # The three seconds interval for ocr pollling.

UPLOAD_DIR = BASE_DIR / "uploaded_images"
WEAKNESS_DIR = BASE_DIR / "uploaded_weakness_images"
RESISTANCE_DIR = BASE_DIR / "uploaded_resistance_images"
MOVES_DIR = BASE_DIR / "uploaded_moves_images"