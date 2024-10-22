from telegram.ext import Application, TypeHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.schedule.schedule import schedule_jobs
from bot.handler.command import start
from bot.handler.message import handle_next_message
from bot.handler.query import main_handler, terms_handler, message_handler, login_handler, self_handler
from bot.handler.filter import check_user_context_data, check_query_message_time


#==> Main bot method
def run(token: str) -> None:
    
    application = Application.builder().token(token).build()
    
    # schedule
    # schedule_jobs(application)
    
    # pre-filter
    application.add_handler(TypeHandler(object, check_user_context_data), group=0)
    
    # query-filter
    application.add_handler(CallbackQueryHandler(check_query_message_time), group=1)

    # commands
    application.add_handler(CommandHandler("start",start), group=2)  
    
    # everything except commands  
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_next_message), group=2)
    
    # query handlers
    application.add_handler(CallbackQueryHandler(terms_handler, pattern="terms*"), group=2)
    application.add_handler(CallbackQueryHandler(message_handler, pattern="message*"), group=2)
    application.add_handler(CallbackQueryHandler(login_handler, pattern="login*"), group=2)
    application.add_handler(CallbackQueryHandler(self_handler, pattern="self*"), group=2)
    application.add_handler(CallbackQueryHandler(main_handler), group=2)
    
    application.run_polling()