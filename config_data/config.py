import os
from dotenv import load_dotenv

load_dotenv()
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")