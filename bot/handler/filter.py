from telegram.ext import CallbackContext, ApplicationHandlerStop
from telegram import Update
from bot.utility import variables as v

#==> Filters
async def check_user_context_data(update: Update, context: CallbackContext) -> None:
    print("first checker")

async def check_query_message_time(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    if message_id != context.user_data.get(v.CONTEXT_LAST_COMMAND_MESSAGE_NUMBER):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)        
        await query.answer("«این پیام منقضی شده»", show_alert=True)
        raise ApplicationHandlerStop()

