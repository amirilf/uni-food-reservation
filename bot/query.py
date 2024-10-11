from telegram import Update
from telegram.ext import CallbackContext
from bot import commands as c
from telegram._callbackquery import CallbackQuery
from database.enums import UserStage
from database.connection import get_async_db_session
from database.user_crud import update_user, get_user_by_t_id
#=======================================

async def is_query_from_old_message(query: CallbackQuery, context: CallbackContext) -> bool:

    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    if message_id != context.user_data["last_command_message"]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")
        
        await query.answer("«این پیام منقضی شده»", show_alert=True)
        return True
    
    return False

async def main_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if await is_query_from_old_message(query, context):
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
    if await is_query_from_old_message(query, context):
        return
    await query.answer()
    
    user_stage = context.user_data.get("user_stage")
    
    match query.data:
        case "terms":
            await c.terms(update, context, user_stage != UserStage.NEW)
        case "terms_accepted":
            if user_stage == UserStage.NEW:
                async with get_async_db_session() as db:
                    try:
                        user = await update_user(db, update.effective_user.id, user_stage=UserStage.TERMS)
                        if user:
                            context.user_data["user_stage"] = UserStage.TERMS
                        else:
                            print("User not found.")
                            return
                    except Exception as db_error:
                        print(f"Database error: {db_error}")
                        return
            else:
                print("wtf is going on? in <terms_accepted> query.")
                return
            await c.start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def message_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    if await is_query_from_old_message(query, context):
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
    if await is_query_from_old_message(query, context):
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
