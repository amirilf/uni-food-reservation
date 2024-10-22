from telegram.ext import CallbackContext
from bot.utility import variables as v
from utility.time import get_tehran_time
from datetime import timedelta
from bot.service.auth import get_authenticated_session
from core.reservation.self import get_food_program

async def update_self_program(context: CallbackContext) -> str | None:
    """
    Try to update the Self week program considering limit and erros.<br>
    If updating was successful store WeekProgram and time in context data & return None, else return the error string<br>
    """
    
    last_update_time = context.user_data.get(v.CONTEXT_USER_SELF_CURRENT_PROGRAM_UPDATE_TIME)
    now = get_tehran_time()
    
    if last_update_time:

        time_difference = now - last_update_time
        if time_difference < timedelta(hours=3):
            return "به تازگی برنامه هفتگیت آپدیت شده، مجددا ۳ ساعت بعد اقدام کن."

    
    session = await get_authenticated_session(context)
    
    # checking for error
    if type(session) == str:
        return session
        
    context.user_data[v.CONTEXT_USER_SELF_CURRENT_PROGRAM_UPDATE_TIME] = now
    context.user_data[v.CONTEXT_USER_SELF_CURRENT_PROGRAM] = get_food_program(session)

    return None
    
async def get_current_week_program(context: CallbackContext) -> str:
      # Assume this fetches the current week's program.
    
    program = context.user_data.get(v.CONTEXT_USER_SELF_CURRENT_PROGRAM)
    
    if not program:
        result = await update_self_program(context)
    
        if result:
            return result
    
    program = context.user_data.get(v.CONTEXT_USER_SELF_CURRENT_PROGRAM)
    current_program = program["current"]
        
    table = []
    
    table.append("روز (تاریخ)       صبحانه                                نهار                                شام")
    
    def process_meal(meal):
        place = meal["place"]["selected"][0]
        food = meal["food"]["selected"][0]
        status = meal["status"]
        return f"{place} | {food} | {status}"
    
    breakfasts = current_program["breakfast"]
    lunches = current_program["lunch"]
    dinners = current_program["dinner"]
    
    for day_index in range(7):
        breakfast = breakfasts[day_index]
        lunch = lunches[day_index]
        dinner = dinners[day_index]
        
        day_with_date = breakfast["day"]

        day_row = f"{day_with_date}    "
        day_row += f"{process_meal(breakfast)}    {process_meal(lunch)}    {process_meal(dinner)}"
        table.append(day_row)

    return "\n".join(table)
