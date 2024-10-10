from utility import config, env
from dotenv import load_dotenv
from bot.bot import run

def main():
    
    # loading .env variables
    if config.DEVELOPMENT: 
        load_dotenv()

    # running bot
    run(env.BOT_TOKEN)

if __name__ == '__main__':
    main()