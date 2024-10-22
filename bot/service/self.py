from telegram.ext import CallbackContext
from bot.utility import variables as v
from utility.time import get_tehran_time
from datetime import timedelta
from bot.service.auth import get_authenticated_session
from core.reservation.self import get_food_program
from requests import Session

async def update_self_program(context: CallbackContext) -> str | None:
    """
    Try to update the Self week program considering limit and erros.<br>
    If updating was successful store WeekProgram and time in context data & return None, else return the error string<br>
    """
    
    last_update_time = context.user_data.get(v.CONTEXT_USER_SELF_PROGRAM_UPDATE_TIME)
    now = get_tehran_time()
    
    if last_update_time:

        time_difference = now - last_update_time
        if time_difference < timedelta(hours=3):
            return "به تازگی برنامه هفتگیت آپدیت شده، مجددا ۳ ساعت بعد اقدام کن."

        # update program
        pass
    
    session = await get_authenticated_session(context)
    
    print(session)
    # error while getting session
    if type(session) == str:
        return session
    
    
    program = get_food_program(session)
    
    context.user_data[v.CONTEXT_USER_SELF_PROGRAM_UPDATE_TIME] = now
    
    print(program)
    return None
    
    
    