from telegram import Update
from telegram.ext import CallbackContext
from bot import commands as c
from telegram._callbackquery import CallbackQuery
#=======================================

async def query_time_checker(query: CallbackQuery, context: CallbackContext) -> bool:

    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    if message_id != c.last_start_message:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")
        
        await query.answer("«این پیام منقضی شده»", show_alert=True)
        return False
    
    return True

async def main_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if not await query_time_checker(query, context):
        return
    await query.answer()
    
    match query.data:
        case 'start':
            await c.start(update, context)
        case 'terms':
            print("HERE IN MAIN")
            await c.terms(update, context)
        case 'usage':
            await c.usage(update, context)
        case 'msg':
            await c.msg(update, context)
        case 'login':
            await c.login(update, context)
        case 'self':
            await c.self(update, context)
        case 'setting':
            await c.setting(update, context)
        case 'profile':
            await c.profile(update, context)
        case 'subscription':
            await c.subscription(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def terms_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if not await query_time_checker(query, context):
        return
    await query.answer()
        
    match query.data:
        case "terms":
            # fetch stage
            stage = c.stage_number
            await c.terms(update, context, stage >= 2)
        case "terms_accepted":
            if c.stage_number < 2:
                c.stage_number = 2
            await c.start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)
