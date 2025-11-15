import time
import yaml
import asyncio
import discord
from Swit.src import Logger
from Swit.src import initialization
from discord.ext import commands
from Swit.src import _add_intents
from Swit.src import path
from Swit.src import _token_valid_check
from Swit.src import download_package

async def StartLoader(app):
    from Swit.src import PluginLoader
    await initialization()
    Logger.LOADER(message=f"Starting Loader..")
    loader_object = PluginLoader(app=app)
    await loader_object.start_loader()



def main():
    with open(path.config(), 'r', encoding='utf-8') as yml_data:
        config = yaml.load(yml_data, Loader=yaml.SafeLoader)

    intents = discord.Intents.default()

    if 'all' in config['discord']['intents']:
        intents = discord.Intents.all()
    else:
        _add_intents(config=config, intents=intents)

    if _token_valid_check(config['discord']['bot_token']) is True:
        Logger.INFO('Downloading required packages...')
        download_package(package_list=config['require']['packages'])
        Logger.INFO('All required packages downloaded!')

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

        asyncio.run(StartLoader(app=app))
        app.run(config['discord']['bot_token'])

    else:
        Logger.ERROR("Invalid token!")
        Logger.INFO("Stop process!")
        return
