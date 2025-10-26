from Swit.SwitSDK import config

async def on_start(app):
    config.make(config_data='assets/config_data.yml')
    print('[Ticket] Starting ticket plugin!')

async def on_stop(app):
    print('[Ticket] Stop ticket plugin!')