from Leafy.LeafySDK import config

async def on_start():
    config.make()
    print('Đã nhận on start')

async def on_stop():
    print('Đã nhận on stop')