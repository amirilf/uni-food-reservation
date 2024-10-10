import os
from dotenv import load_dotenv
from bot.utility import variables as v

if v.DEVELOPMENT: 
    print("loading .env variables")
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
