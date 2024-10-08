from telegram import Update
from telegram.ext import CallbackContext
from bot import commands as c
#=======================================

# TODO: in all queries check for the message.id, if not equal to the last start command message
# TODO: then it's completely obvious that is an old message!

async def main_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
    
    match query.data:
        case 'start':
            await c.start(update, context)
        case 'terms':
            print("HERE IN MAIN")
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
        case _:
            raise Exception("Wrong query data: " + query.data)


async def terms_handler(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    await query.answer()
    
    
    match query.data:
        case "terms":
            # fetch stage
            stage = c.stage_number
            await c.terms(update, context, stage >= 2)
        case "terms_accepted":
            if c.stage_number < 2:
                c.stage_number = 2
            await c.start(update, context)
        case _:
            raise Exception("Wrong query data: " + query.data)
