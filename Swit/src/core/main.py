#MIT License

#Copyright (c) 2025 kenftr

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import time
import yaml
import asyncio
import discord
from discord.ext import commands
from Swit.src import _add_intents
from Swit.src import path
from Swit.src import Loader
from Swit.src import Logger
from Swit.src import initialization
from Swit.src import _token_valid_check
from Swit.src import download_package

async def start_loader(app):
    await initialization()
    Logger.LOADER(message=f"Starting Loader..")
    init_loader = Loader(app=app)
    await init_loader.start_loader()

def main():
    with open(path.config(), 'r', encoding='utf-8') as yml_data:
        config = yaml.load(yml_data, Loader=yaml.SafeLoader)
    intents = discord.Intents.default()

    if 'all' in config['discord']['intents']:
        intents = discord.Intents.all()
    else:
        _add_intents(config=config, intents=intents)

    if config['discord']['auto_sharded'].lower() == 'enable' or config['discord']['auto_sharded'] == True:
        app = commands.AutoShardedBot(
            command_prefix=config['discord'].get('command_prefix', '!'),
            intents=intents,
        )
    else:
        app = commands.Bot(
            command_prefix=config['discord'].get('command_prefix', '!'),
            intents=intents,
        )

    @app.event
    async def on_ready():
        start_time = time.time()
        stop_time = time.time()
        Logger.LOADER(message=f"Load all plugin in {round(stop_time - start_time, 3)}s!")
        Logger.INFO(message=f"Waiting for sync...")
        await app.tree.sync()
        Logger.INFO(message=f"Sync done after {round(time.time() - stop_time, 2)}s!")
        Logger.INFO(message=f'The startup process takes a total: {round(time.time() - start_time, 2)}s!')

    if _token_valid_check(config['discord']['bot_token']) == True:
        Logger.INFO('Download default package')
        download_package(package_list=config['require']['packages'])
        asyncio.run(start_loader(app=app))
        app.run(config['discord']['bot_token'])
    else:
        Logger.ERROR(f"Invalid token!")
        Logger.INFO(f"Stop process!")
        return
