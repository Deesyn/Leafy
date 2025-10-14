import time

import yaml
import discord
from discord.ext import commands
from Moss.src.local import _add_intents
from Moss.src.utils.file_handler.path_manager import path
from Moss.src.utils.Local_Logger import Logger
from Moss.src.utils.token_valid_check import _token_valid_check
from Moss.src.loader.handler.download_package import download_package
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
        from Moss.src.loader.loader import Loader
        start_time = time.time()
        Logger.LOADER(message=f"Starting Loader..")
        init_loader = Loader(app=app)
        await init_loader.start_loader()
        stop_time = time.time()
        Logger.LOADER(message=f"Load all plugin in {round(stop_time - start_time, 5)}s!")
        Logger.INFO(message=f"Waiting for sync...")
        await app.tree.sync()
        Logger.INFO(message=f"Sync done after {round(time.time() - stop_time, 2)}s!")
        Logger.INFO(message=f'The startup process takes a total: {round(time.time() - start_time,2)}s!')

    if _token_valid_check(config['discord']['bot_token']) == True:
        Logger.INFO('Download default package')
        download_package(package_list=config['require']['packages'])
        app.run(config['discord']['bot_token'])
    else:
        Logger.ERROR(f"Invalid token!")
        Logger.INFO(f"Stop process!")
        return
