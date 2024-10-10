from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.schedule import schedule_jobs
from bot.commands import start_command, handle_next_message
from bot.query import main_handler, terms_handler, message_handler, login_handler
#=======================================

def run(token: str) -> None:
    
    application = Application.builder().token(token).build()
    
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