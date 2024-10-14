from database.connection import get_async_db_session
from database.user_crud import create_user, get_user_by_t_id
from database.enums import UserStage
from telegram import Update
from telegram.ext import CallbackContext
from bot.utility import keyboards as k, variables as v
from bot.utility.texts import texts as t


#==> Commands
async def start(update: Update, context: CallbackContext) -> None:  
        
    # check if there is a last command message to delete
    last_command_message = context.user_data.get(v.CONTEXT_LAST_COMMAND_MESSAGE_NUMBER)
    if last_command_message:
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_command_message)
        except Exception as e:
            print(f"Error deleting last message: {e}")

    user_stage = context.user_data.get(v.CONTEXT_USER_STAGE)
    
    # check if it's a new user
    if not user_stage:
        # seems like it's a new user
        
        # get user data
        user = update.effective_user 
        t_id = user.id   
        t_fullname = user.full_name
        
        async with get_async_db_session() as db:
            try:
                existing_user = await get_user_by_t_id(db, t_id)
                if existing_user:
                    user_stage = existing_user.user_stage
                    context.user_data[v.CONTEXT_USER_STAGE] = user_stage
                else:
                    new_user = await create_user(db, t_id=t_id, t_fullname=t_fullname)
                    if new_user:
                        user_stage = UserStage.NEW
                        context.user_data[v.CONTEXT_USER_STAGE] = user_stage
                    else:
                        print("Failed creating a new user.")
                        await update.message.reply_text("Failed.")
                        return
            except Exception as db_error:
                print(f"Database error: {db_error}")
                await update.message.reply_text("Failed.")
                return
    
    # set markup & text
    reply_markup = k.get_main_keyboard(user_stage.value)
    reply_text = t[f"stage{user_stage.value}"]

    new_message = await update.message.reply_text(text=reply_text, reply_markup=reply_markup)

    # save command message id
    context.user_data[v.CONTEXT_LAST_COMMAND_MESSAGE_NUMBER] = new_message.message_id
