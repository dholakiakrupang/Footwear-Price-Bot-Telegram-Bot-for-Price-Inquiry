import os

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise ValueError("No TELEGRAM_API_TOKEN found in environment variables")

APPROVED_USERS = ["dholakiakrupang","Dhruvilathigara","dhirendradholakia"]  # List of approved users
SPECIAL_USERS = ["dholakiakrupang"]  # List of special users
ADMIN_USERS = ["admin_user"]  # List of admin users
