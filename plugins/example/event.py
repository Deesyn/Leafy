from discord.ext import commands
from Azurite.AzuriteSDK import config

async def on_start():
    print('Đã nhận on start')

async def on_stop():
    print('Đã nhận on stop')