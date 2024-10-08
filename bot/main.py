import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.utility import variables as v, env
from bot.schedule import schedule_jobs
#=======================================


# set system proxy if needed
if v.PROXY:
    os.environ['http_proxy'] = 'http://192.168.175.26:8080'
    os.environ['https_proxy'] = 'http://192.168.175.26:8080'

def main():
    application = Application.builder().token(env.API_TOKEN).build()    
    schedule_jobs(application)
    application.run_polling()

if __name__ == '__main__':
    main()
