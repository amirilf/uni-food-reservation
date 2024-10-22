from telegram.ext import CallbackContext
import requests
from bot.utility import variables as v
from database.config.connection import get_async_db_session
from database.repository.user_repository import get_user_by_t_id, update_user
from database.model.enums import UserStage
from core.account import auth as core_auth, profile as core_profile
from utility.config import CULLINAN_COOKIE_NAME


#========> Auth service methods
async def save_profile_info(context: CallbackContext, t_id: int) -> None:
    """
    This methods assumes that the context has the session and the session is authenticated!!!
    This method is responsible to fetch user profile from website and then save its information in db and context
    """

    try:

        session = context.user_data.get(v.CONTEXT_USER_SESSION)
        cookie = session.cookies.get(CULLINAN_COOKIE_NAME)

        result = core_profile.get_profile_information(session)

        async with get_async_db_session() as db:
            user = await update_user(db, t_id, 
                                    user_stage=UserStage.LOGIN,
                                    fullname=result.get("fullname"),
                                    gender=result.get("gender"),
                                    national_number=result.get("national_number"),
                                    phone=result.get("phone"),
                                    email=result.get("email"),
                                    faculty=result.get("faculty"),
                                    cookie=cookie)
            if not user:
                print("User not updated in <save_profile_info>")
            else:
                context.user_data[v.CONTEXT_USER_T_ID] = user.t_id
                context.user_data[v.CONTEXT_USER_USERNAME] = user.username
                context.user_data[v.CONTEXT_USER_FULLNAME] = user.fullname
                
    except Exception as e:
        print(e)
    
async def login_process(context: CallbackContext, t_id: int, username: str, password: str) -> str | None:
    # TODO: check limitation of login process
    
    try:
        session = core_auth.login(username, password)
        async with get_async_db_session() as db:
            try:
                user = await update_user(db, t_id, user_stage=UserStage.LOGIN, username=username, password=password)
                if user:
                    context.user_data[v.CONTEXT_USER_STAGE] = UserStage.LOGIN
                    context.user_data[v.CONTEXT_USER_SESSION] = session
                    return None
                else:
                    print("User not found.")
                    return "Failed."
            except Exception as db_error:
                print(f"Database error: {db_error}")
                return "Failed."
    except Exception as e:
        return str(e)

async def get_session(context: CallbackContext) -> requests.Session | None:

    session = context.user_data.get(v.CONTEXT_USER_SESSION)

    if session:
        return session
    
    async with get_async_db_session() as db:
        user = await get_user_by_t_id(db, context.user_data.get(v.CONTEXT_USER_T_ID))
        if user:
            session = requests.Session()
            session.cookies.set(CULLINAN_COOKIE_NAME, user.cookie)
            context.user_data[v.CONTEXT_USER_SESSION] = session
            return session
        else:
            print("User not found.")
            return None
    
async def get_authenticated_session(context: CallbackContext) -> requests.Session | str:
    
    session = await get_session(context)
    
    if session:
        if core_auth.session_checker(session):
            print("Session was ok.")
            return session
    
    print("Trying to get new session")
    try:
        # login & get new session
        print(context.user_data[v.CONTEXT_USER_USERNAME])
        print(context.user_data[v.CONTEXT_USER_PASSWORD])
        
        session = core_auth.login(context.user_data[v.CONTEXT_USER_USERNAME], context.user_data[v.CONTEXT_USER_PASSWORD])
        
        # save in db
        cookie = session.cookies.get(CULLINAN_COOKIE_NAME)
        async with get_async_db_session() as db:
            user = await update_user(db, context.user_data[v.CONTEXT_USER_T_ID], cookie = cookie)
            if not user:
                print("User not updated in <get_authenticated_session>")
            else:
                context.user_data[v.CONTEXT_USER_SESSION] = session
    
        return session
    
    except Exception as e:
        return str(e)
    