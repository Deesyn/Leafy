from Swit.sdk import config

async def on_start(app):
    config.make(config_data='assets/config_data.yml')
    print('Đã nhận on start')

async def on_stop(app):
    print('Đã nhận on stop')