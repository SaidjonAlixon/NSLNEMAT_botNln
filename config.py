import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8066936618:AAEhS_eMO_EzzH8AzSJXo8WVr6gjMpfyPkc')

# Google Sheets ID
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID', '1PwXbGkPGR8_EHE9sIPZcE3vW7wLWEH-CHViBjvMp_fA')

# Google Sheets worksheet names - bu nomlar Google Sheets da mavjud bo'lishi kerak
# Agar worksheet nomlari boshqacha bo'lsa, ularni o'zgartiring
ORDERS_SHEET = os.getenv('ORDERS_SHEET', 'List1')  # Buyurtmalar worksheet nomi
USERS_SHEET = os.getenv('USERS_SHEET', 'List3')   # Foydalanuvchilar worksheet nomi

# Railway environment variables
RAILWAY_ENVIRONMENT = os.getenv('RAILWAY_ENVIRONMENT', False)
RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', '') 