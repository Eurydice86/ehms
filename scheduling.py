import schedule
import datetime

from ehms_mc_api.src import initialise
from ehms_discord_bot.src_bot import bot

def test(message):
    print(message)

schedule.every().sunday.at("00:00").do(initialise.run)

schedule.every().day.at("16:30").do(bot.presences)
schedule.every().monday.at("07:30")(bot.inactive)

while True:
    schedule.run_pending()
