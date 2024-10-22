from telegram import Update
from telegram.ext import CallbackContext
from database.enums import UserStage
from database.connection import get_async_db_session
from database.user_crud import update_user
from bot.utility import keyboards as k, variables as v
from bot.utility.texts import texts as t, get_profile_text


#==> Query handlers
async def main_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
    
    match query.data:
        case 'start':
            await start(update, context)
        case 'usage':
            await usage(update, context)
        case 'setting':
            await setting(update, context)
        case 'profile':
            await profile(update, context)
        case 'subscription':
            await subscription(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def terms_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
    
    user_stage = context.user_data.get(v.CONTEXT_USER_STAGE)
    
    match query.data:
        case "terms":
            await terms(update, context, user_stage != UserStage.NEW)
        case "terms_accepted":
            if user_stage == UserStage.NEW:
                async with get_async_db_session() as db:
                    try:
                        user = await update_user(db, update.effective_user.id, user_stage=UserStage.TERMS)
                        if user:
                            context.user_data[v.CONTEXT_USER_STAGE] = UserStage.TERMS
                        else:
                            print("User not found.")
                            return
                    except Exception as db_error:
                        print(f"Database error: {db_error}")
                        return
            else:
                print("wtf is going on? in <terms_accepted> query.")
                return
            await start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def message_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    
    match query.data:
        case 'message':
            # check for limitation (fetching from the redis or context.user_data)
            is_limited = False
            if is_limited:
                await query.answer("«به محدودیت ارسال پیام رسیدی، بعدا امتحان کن»", show_alert=True)
            else:
                await query.answer()
                await message(update, context)
        case "message_cancel":
            await query.answer()
            context.user_data[v.CONTEXT_NEXT_MESSAGE_FORWARD] = False
            await start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def login_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    
    match query.data:
        case 'login':
            # check for limitation (fetching from the redis or context.user_data)
            is_limited = False
            if is_limited:
                await query.answer("«به محدودیت ورود به سامانه رسیدی، بعدا امتحان کن»", show_alert=True)
            else:
                await query.answer()
                await login(update, context)
        case "login_cancel":
            await query.answer()
            # TODO: make these keys variables
            context.user_data[v.CONTEXT_NEXT_MESSAGE_LOGIN] = False
            await start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)

async def self_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
        
    match query.data:
        case 'self':
            await self(update, context)
        case "self_manual":
            print("manual")
        case "self_automatic":
            print("auto")
        case "self_program":
            print("program")
        case "self_priority":
            print("priority")
        case _:
            raise Exception("Wrong query data: " + query.data)


#==> Query methods
async def start(update: Update, context: CallbackContext) -> None:
    user_stage = context.user_data[v.CONTEXT_USER_STAGE]
    await update.callback_query.edit_message_text(t[f"stage{user_stage.value}"],reply_markup=k.get_main_keyboard(user_stage.value))

async def terms(update: Update, context: CallbackContext, accepted: bool) -> None:  
    
    if accepted:
        reply_markup = k.get_back_keyboard("start")
    else:
        reply_markup = k.terms_keyboard
      
    await update.callback_query.edit_message_text(text=t["terms"], reply_markup=reply_markup)
    
async def usage(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["usage"], reply_markup=k.get_back_keyboard("start"))

async def message(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["message"], reply_markup=k.get_back_keyboard("message_cancel"))
    context.user_data[v.CONTEXT_NEXT_MESSAGE_FORWARD] = True

async def login(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["login"], reply_markup=k.get_back_keyboard("login_cancel"))
    context.user_data[v.CONTEXT_NEXT_MESSAGE_LOGIN] = True

async def profile(update: Update, context: CallbackContext) -> None:
    
    try:
        fullname = context.user_data[v.CONTEXT_USER_FULLNAME]
        username = context.user_data[v.CONTEXT_USER_USERNAME]
        await update.callback_query.edit_message_text(get_profile_text(fullname, username),reply_markup=k.get_back_keyboard("start"))
        
    except:
        print("ERROR FETCHING PROFILE INFO.")
        await update.callback_query.answer("عملیات ناموفق.", show_alert=True)    

async def self(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["self"], reply_markup=k.self_keyboard)

async def setting(update: Update, context: CallbackContext) -> None:
    pass
        
async def subscription(update: Update, context: CallbackContext) -> None:
    pass

