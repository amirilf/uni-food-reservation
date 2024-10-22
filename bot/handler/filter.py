from telegram.ext import CallbackContext, ApplicationHandlerStop
from telegram import Update
from bot.utility import variables as v
from database.connection import get_async_db_session
from database.user_crud import get_user_by_t_id, create_user
from database.enums import UserStage
import requests
from utility.config import CULLINAN_COOKIE_NAME


#==> Filters
async def check_user_context_data(update: Update, context: CallbackContext) -> None:
    """
    Check all the updates first here, trying to be sure all needed user infos are available
    in context.user_data to work without problem in other methods.
    """
    # TODO: check limits in a 0 group method for login, spam, even black list and stuff like them.

    user_data_available = context.user_data.get(v.CONTEXT_USER_DATA_AVAILABLE, False)
    
    if user_data_available:
        return
    
    print("User has not enough info", end=" & ")
    
    # not sure if we have all data we need
    
    t_id = update.effective_user.id    
    context.user_data[v.CONTEXT_USER_T_ID] = t_id
    
    # check if user is already in db or not
    async with get_async_db_session() as db:
        try:
            user = await get_user_by_t_id(db, t_id)
            
            if user:
                print("already existed")
                context.user_data[v.CONTEXT_USER_STAGE] = user.user_stage
                if user.user_stage.value >= UserStage.LOGIN.value:
                    context.user_data[v.CONTEXT_USER_USERNAME] = user.username
                    context.user_data[v.CONTEXT_USER_PASSWORD] = user.password
                    context.user_data[v.CONTEXT_USER_FULLNAME] = user.fullname
                    if user.cookie:
                        session = requests.Session()
                        session.cookies.set(CULLINAN_COOKIE_NAME, user.cookie)
                        context.user_data[v.CONTEXT_USER_SESSION] = session
            else:
                # it's a new user
                print("is new")
                user = await create_user(db, t_id)
                context.user_data[v.CONTEXT_USER_STAGE] = UserStage.NEW
        
        except Exception as db_error:
            print(f"Database error: {db_error}")

    # we did our best to provide infos so here we are
    context.user_data[v.CONTEXT_USER_DATA_AVAILABLE] = True

async def check_query_message_time(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    if message_id != context.user_data.get(v.CONTEXT_LAST_COMMAND_MESSAGE_ID):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)        
        await query.answer("«این پیام منقضی شده»", show_alert=True)
        raise ApplicationHandlerStop()
