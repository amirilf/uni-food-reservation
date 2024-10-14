from telegram.ext import CallbackContext
from telegram.ext import Application
from utility import env, config
#=======================================

async def bot_is_alive(context: CallbackContext):
    await context.bot.send_message(chat_id=env.ADMIN_ID, text=f"Bot is alive.")

async def reserve(context: CallbackContext):
    await context.bot.send_message(chat_id=env.ADMIN_ID, text=f"Going to reserve.")

def schedule_jobs(application: Application):
    job_queue = application.job_queue
        
    job_queue.run_daily(
        reserve,
        time=config.RESERVE_TIME,
        days=config.RESERVE_DAY,
        name="reserve"
    )

    job_queue.run_repeating(
        bot_is_alive, 
        interval=10,
        first=0,
        name="is_alive"
    )