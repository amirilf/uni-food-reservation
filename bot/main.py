import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.utility import variables as v, env
from bot.schedule import schedule_jobs
from bot.commands import start_command, handle_next_message
from bot.query import main_handler, terms_handler, message_handler, login_handler
from dotenv import load_dotenv
#=======================================

# load .env variables
if v.ENV == "DEVELOPMENT":
    load_dotenv()

def main():
    application = Application.builder().token(env.BOT_TOKEN).build()
    
    # schedule
    # schedule_jobs(application)
    
    # commands
    application.add_handler(CommandHandler("start",start_command))  
    
    # everything except commands  
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_next_message))
    
    # query handlers
    application.add_handler(CallbackQueryHandler(terms_handler, pattern="terms*"))
    application.add_handler(CallbackQueryHandler(message_handler, pattern="message*"))
    application.add_handler(CallbackQueryHandler(login_handler, pattern="login*"))
    application.add_handler(CallbackQueryHandler(main_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()
