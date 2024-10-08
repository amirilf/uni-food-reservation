from telegram import Update
from telegram.ext import CallbackContext
from bot import keyboards as k
from bot.texts import texts as t
#=======================================

last_start_message = None
stage_number = 0

async def start_command(update: Update, context: CallbackContext) -> None:
    # 1. check for limitation of usage start command in redis

    # 2. fetch these stuff from the db (postgres or redis)
    global last_start_message
    global stage_number
    

    # 3. remove last command message before sending new one.
    if last_start_message:
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_start_message)
        except Exception as e:
            print(f"Error deleting last message: {e}")
    
    # 4. create user in db if it's the first time
    if stage_number == 0:
        stage_number = 1
    
    # 5. set text and markup keyboard based on the user stage
    reply_markup = k.get_main_keyboard(stage_number)
    reply_text = t[f"stage{stage_number}"]

    new_message = await update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    
    # 6. save command message id
    last_start_message = new_message.message_id

async def start(update: Update, context: CallbackContext) -> None:
    
    # fetch stage from db
    global stage_number
    
    await update.callback_query.edit_message_text(t[f"stage{stage_number}"],reply_markup=k.get_main_keyboard(stage_number))

async def terms(update: Update, context: CallbackContext, accepted: bool) -> None:  
    
    if accepted:
        reply_markup = k.get_back_keyboard("start")
    else:
        reply_markup = k.terms_keyboard
      
    await update.callback_query.edit_message_text(text=t["terms"], reply_markup=reply_markup)
    
async def usage(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["usage"], reply_markup=k.get_back_keyboard("start"))

async def msg(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["msg"], reply_markup=k.get_back_keyboard("start"))

async def login(update: Update, context: CallbackContext) -> None:
    pass

async def self(update: Update, context: CallbackContext) -> None:
    pass

async def setting(update: Update, context: CallbackContext) -> None:
    pass

async def profile(update: Update, context: CallbackContext) -> None:
    pass

async def subscription(update: Update, context: CallbackContext) -> None:
    pass
