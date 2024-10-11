from utility import config, env
from dotenv import load_dotenv
from bot.bot import run
from database.init_db import init_db

def main():

    # loading .env variables
    if config.DEVELOPMENT: 
        load_dotenv()
        
    # db
    init_db()

    # running bot
    run(env.BOT_TOKEN)

if __name__ == '__main__':
    main()