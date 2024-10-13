import schedule
import datetime

from ehms_mc_api.src import initialise
from ehms_discord_bot.src_bot import bot

def test(message):
    print(message)

schedule.every().sunday.at("14:48").do(initialise.run)

schedule.every(1).minutes.do(bot.presences)
schedule.every(1).minutes.do(bot.inactive)

while True:
    schedule.run_pending()
