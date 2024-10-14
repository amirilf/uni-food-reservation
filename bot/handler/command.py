from telegram import Update
from telegram.ext import CallbackContext
from bot.utility import keyboards as k, variables as v
from bot.utility.texts import texts as t


#==> Commands
async def start(update: Update, context: CallbackContext) -> None:  
    
    user_stage = context.user_data.get(v.CONTEXT_USER_STAGE)
    
    reply_text = t[f"stage{user_stage.value}"]
    reply_markup = k.get_main_keyboard(user_stage.value)
    
    new_message = await update.message.reply_text(text=reply_text, reply_markup=reply_markup)

    # save command message_id to check old queries using that
    context.user_data[v.CONTEXT_LAST_COMMAND_MESSAGE_ID] = new_message.message_id
