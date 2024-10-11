from telegram import Update
from telegram.ext import CallbackContext
import requests
from bot import keyboards as k
from bot.texts import texts as t, get_profile_text
from utility import env
from database.connection import get_async_db_session
from database.user_crud import create_user, get_user_by_t_id, update_user
from database.enums import UserStage
from core.account import auth as core_auth, profile as core_profile
#=======================================

# Command methods
async def start_command(update: Update, context: CallbackContext) -> None:  
    
    # check if there is a last command message to delete
    last_command_message = context.user_data.get("last_command_message")
    if last_command_message:
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_command_message)
        except Exception as e:
            print(f"Error deleting last message: {e}")

    user_stage = context.user_data.get("user_stage")
    
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
                    context.user_data["user_stage"] = user_stage
                else:
                    new_user = await create_user(db, t_id=t_id, t_fullname=t_fullname)
                    if new_user:
                        user_stage = UserStage.NEW
                        context.user_data["user_stage"] = user_stage
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
    context.user_data["last_command_message"] = new_message.message_id


# Query methods
async def start(update: Update, context: CallbackContext) -> None:
    user_stage = context.user_data["user_stage"]
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
    context.user_data['forward_next_message'] = True

async def login(update: Update, context: CallbackContext) -> None:
    await update.callback_query.edit_message_text(text=t["login"], reply_markup=k.get_back_keyboard("login_cancel"))
    context.user_data['login_next_message'] = True

async def self(update: Update, context: CallbackContext) -> None:
    pass

async def setting(update: Update, context: CallbackContext) -> None:
    pass

async def profile(update: Update, context: CallbackContext) -> None:
    
    t_id = update.effective_user.id

    try:
        async with get_async_db_session() as db:
            try:
                user = await get_user_by_t_id(db, t_id)
                if user:
                    await update.callback_query.edit_message_text(text=get_profile_text(user.fullname, user.username, user.faculty), reply_markup=k.get_back_keyboard("start"))
                else:
                    print("User not found.")
            except Exception as db_error:
                print(f"Database error: {db_error}")
    except Exception as e:
        print(e)
    
    await update.callback_query.answer("عملیات ناموفق.", show_alert=True)    

async def subscription(update: Update, context: CallbackContext) -> None:
    pass


# Message methods 
async def handle_next_message(update: Update, context: CallbackContext) -> None:

    if context.user_data.get('forward_next_message', False):
        await forward_message_to_admin(update, context)        

    elif context.user_data.get("login_next_message", False):
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
    
    context.user_data['forward_next_message'] = False

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
    context.user_data["login_next_message"] = False


    await update.message.reply_text(login_error if login_error else "ورود با موفقیت انجام شد.")        
    await start_command(update, context)
      
    # =====> fetch & save profile  
    session = context.user_data.get("user_session")
    
    for i in range(5):
        try:
            await save_profile_info(session, t_id)
            return
        except Exception as e:
            print("Exception in saving informations of the user,", t_id)
        
async def save_profile_info(session: requests.Session, t_id: int) -> None:
    try:
        result = core_profile.get_profile_information(session)
        async with get_async_db_session() as db:
            user = await update_user(db, t_id, 
                                    user_stage=UserStage.LOGIN,
                                    fullname=result.get("fullname"),
                                    gender=result.get("gender"),
                                    national_number=result.get("national_number"),
                                    phone=result.get("phone"),
                                    email=result.get("email"),
                                    faculty=result.get("faculty"))
            if not user:
                print("User not updated in <save_profile_info>")
    except:
        print("User not updated in <save_profile_info>")
    
async def login_process(context: CallbackContext, t_id: int, username: str, password: str) -> str | None:
    # TODO: check limitation of login process
    
    try:
        session = core_auth.login(username, password)
        async with get_async_db_session() as db:
            try:
                user = await update_user(db, t_id, user_stage=UserStage.LOGIN, username=username, password=password)
                if user:
                    context.user_data["user_stage"] = UserStage.LOGIN
                    context.user_data["user_session"] = session
                    return None
                else:
                    print("User not found.")
                    return "Failed."
            except Exception as db_error:
                print(f"Database error: {db_error}")
                return "Failed."
    except Exception as e:
        return str(e)
