from telegram import Update
from telegram.ext import CallbackContext
from bot.utility import variables as v
from utility import env
from bot.handler.command import start
from bot.service.auth import login_process, save_profile_info


#==> Message handlers
async def handle_next_message(update: Update, context: CallbackContext) -> None:

    if context.user_data.get(v.CONTEXT_NEXT_MESSAGE_FORWARD, False):
        await forward_message_to_admin(update, context)        

    elif context.user_data.get(v.CONTEXT_NEXT_MESSAGE_LOGIN, False):
        await login_user_in_cullinan(update, context)

async def forward_message_to_admin(update: Update, context: CallbackContext) -> None:
    
    admin_chat_id = env.ADMIN_ID
    
    forwarded_message = await update.message.forward(chat_id=admin_chat_id)
    
    user = update.message.from_user
    user_link = f"[{user.full_name}](tg://user?id={user.id})"
    
    await context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"By {user_link} with id: {user.id}.",
        reply_to_message_id=forwarded_message.message_id,
        parse_mode='Markdown'
    )
    
    await update.message.reply_text("با موفقیت به ادمین ارسال شد.", reply_to_message_id=update.message.message_id)
    
    context.user_data[v.CONTEXT_NEXT_MESSAGE_FORWARD] = False

async def login_user_in_cullinan(update: Update, context: CallbackContext) -> None:

    # =====> message validation
    if update.message.text is None:
        await update.message.reply_text("باید یک متن شامل نام کاربری و رمزعبورت ارسال کنی!")
        return

    lines = update.message.text.strip().split("\n")

    if len(lines) != 2:
        await update.message.reply_text("فرمت ورودی رو یادت رفته؟ (خط اول نام کاربری و خط دوم رمزعبورت)")
        return

    username = lines[0].strip()
    password = lines[1].strip()

    if not username or not password:
        await update.message.reply_text("لطفا یک نام کاربری و رمزعبور با فرمت صحیح برام بفرست.")
        return

    await update.message.reply_text("درحال تلاش برای ورود به سامانه...")  
    
    
    # =====> trying to login
    t_id = update.effective_user.id
    login_error = await login_process(context, t_id, username, password)
    context.user_data[v.CONTEXT_NEXT_MESSAGE_LOGIN] = False


    await update.message.reply_text(login_error if login_error else "ورود با موفقیت انجام شد.")        
    await start(update, context)
    
    if not login_error:
        for i in range(5):
            try:
                await save_profile_info(context, t_id)
                return
            except Exception as e:
                print("Exception in saving informations of the user,", t_id)
