from telegram.ext import CallbackContext
from bot.utility import variables as v
from utility.time import get_tehran_time
from datetime import timedelta
from bot.service.auth import get_authenticated_session
from core.reservation.self import get_food_program
from utility.image import generate_current_program_image
from utility.config import USER_MEDIA_PATH

async def update_current_self_program(context: CallbackContext) -> str | None:
    """
    Try to update the Self week program considering limit and erros.<br>
    If updating was successful store WeekProgram and time in context data & return None, else return the error string<br>
    """
    
    last_update_time = context.user_data.get(v.CONTEXT_USER_SELF_CURRENT_PROGRAM_UPDATE_TIME)
    now = get_tehran_time()
    
    if last_update_time:

        time_difference = now - last_update_time
        if time_difference < timedelta(hours=1):
            return "به تازگی برنامه هفتگیت آپدیت شده، مجددا یک ساعت بعد اقدام کن."

    
    session = await get_authenticated_session(context)
    
    # checking for error
    if type(session) == str:
        return session

    context.user_data[v.CONTEXT_USER_SELF_CURRENT_PROGRAM_UPDATE_TIME] = now
    
    # get current week program data
    program_data = get_food_program(session)
    context.user_data[v.CONTEXT_USER_SELF_CURRENT_PROGRAM] = program_data
    
    # generate image
    current_program = program_data["current"]

    def process_meal(meal):
        place = meal["place"]["selected"][0]
        food = meal["food"]["selected"][0]
        status = meal["status"]
        return [food, place, status]
        
    breakfasts = current_program["breakfast"]
    lunches = current_program["lunch"]
    dinners = current_program["dinner"]
    
    program_flat_detail = []
    
    for day_index in range(7):
        breakfast = breakfasts[day_index]
        lunch = lunches[day_index]
        dinner = dinners[day_index]
        day_with_date = breakfast["day"]
        program_flat_detail.append([day_with_date, [process_meal(breakfast), process_meal(lunch), process_meal(dinner)]])

    generate_current_program_image(program_flat_detail).save(f"{USER_MEDIA_PATH}{context.user_data[v.CONTEXT_USER_T_ID]}.png")

    return None
    
async def get_current_self_program(context: CallbackContext) -> str | None:
    
    if not context.user_data.get(v.CONTEXT_USER_SELF_CURRENT_PROGRAM):
    
        result = await update_current_self_program(context)
    
        if result:
            return result
    
    return None
