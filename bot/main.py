import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.utility import variables as v, env
from bot.schedule import schedule_jobs
from bot.commands import start_command, forward_message_to_admin
from bot.query import main_handler, terms_handler, message_handler
#=======================================


# set system proxy if needed
if v.PROXY:
    os.environ['http_proxy'] = 'http://192.168.175.26:8080'
    os.environ['https_proxy'] = 'http://192.168.175.26:8080'

def main():
    application = Application.builder().token(env.API_TOKEN).build()
    
    # schedule_jobs(application)
    
    application.add_handler(CommandHandler("start",start_command))    
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message_to_admin))
    
    application.add_handler(CallbackQueryHandler(terms_handler, pattern="terms*"))
    application.add_handler(CallbackQueryHandler(message_handler, pattern="message*"))
    application.add_handler(CallbackQueryHandler(main_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()
