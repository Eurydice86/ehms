import config

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os

import monthly_presences, inactive_members


def presences():
    load_dotenv()
    presences_channel_id = int(os.getenv("PRESENCES_CHANNEL_ID"))
    bot_token = os.getenv("BOT_TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot("!", intents=intents)

    @bot.event
    async def on_ready():
        presences_channel = bot.get_channel(presences_channel_id)
        await presences_channel.send(monthly_presences.monthly_presences())
        await bot.close()

    bot.run(token=bot_token)


def inactive():
    load_dotenv()
    inactive_channel_id = int(os.getenv("INACTIVE_CHANNEL_ID"))
    bot_token = os.getenv("BOT_TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot("!", intents=intents)

    @bot.event
    async def on_ready():
        inactive_channel = bot.get_channel(inactive_channel_id)
        m1, m2 = inactive_members.inactive_members()
        await inactive_channel.send(m1)
        for m in m2:
            await inactive_channel.send(m)
        await bot.close()

    bot.run(token=bot_token)
