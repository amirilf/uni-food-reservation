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
        case 'usage':
            await c.usage(update, context)
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

async def message_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if not await query_time_checker(query, context):
        return
    
    match query.data:
        case 'message':
            # check for limitation (fetching from the redis or context.user_data)
            is_limited = False
            if is_limited:
                await query.answer("«به محدودیت ارسال پیام رسیدی، بعدا امتحان کن»", show_alert=True)
            else:
                await query.answer()
                await c.message(update, context)
        case "message_cancel":
            await query.answer()
            context.user_data['forward_next_message'] = False
            await c.start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def login_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if not await query_time_checker(query, context):
        return
    
    match query.data:
        case 'login':
            # check for limitation (fetching from the redis or context.user_data)
            is_limited = False
            if is_limited:
                await query.answer("«به محدودیت ورود به سامانه رسیدی، بعدا امتحان کن»", show_alert=True)
            else:
                await query.answer()
                await c.login(update, context)
        case "login_cancel":
            await query.answer()
            # TODO: make these keys variables
            context.user_data['login_next_message'] = False
            await c.start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)
