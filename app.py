from utility import config, env, file
from dotenv import load_dotenv
from bot import bot
from database.init_db import init_db

def main():

    # remove pycashe files
    file.remove_pycaches()

    # loading .env variables
    if config.DEVELOPMENT: 
        load_dotenv()
        
    # db
    init_db()

    # running bot
    bot.run(env.BOT_TOKEN)

if __name__ == '__main__':
    main()