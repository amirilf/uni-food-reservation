from telegram import Update
from telegram.ext import CallbackContext
from bot import commands as c
#=======================================

async def main_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
    
    match query.data:
        case 'start':
            await c.start(update, context)
        case 'terms':
            await c.terms(update, context)
        case 'usage':
            await c.usage(update, context)
        case 'msg':
            await c.msg(update, context)
        case 'login':
            await c.login(update, context)
        case 'self':
            await c.self(update, context)
        case 'setting':
            await c.setting(update, context)
        case 'profile':
            await c.profile(update, context)
        case 'subscription':
            await c.subscription(update, context)

    raise Exception("Wrong query data: " + query.data)
