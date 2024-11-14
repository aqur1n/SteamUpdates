# -*- coding: utf-8 -*-

import logging
from time import sleep
from json import loads, dumps
from os.path import exists, dirname, realpath
from os import chdir

from discord import SyncWebhook

from steam.client.cdn import CDNClient
from steam.client import SteamClient

from modules.embeds import embed_updated_bch, embed_created_bch


logging.basicConfig(
    level = logging.INFO,
    format = r'[%(asctime)s] [%(levelname)s]  %(message)s',
)
logger = logging.getLogger(__name__)

chdir(dirname(realpath(__file__)))
try:
    with open('config.json', encoding = 'utf-8') as f:
        cfg = loads(f.read())
    APP_ID = cfg['app_id']
    DISCORD_WEBHOOK = SyncWebhook.from_url(cfg['discord_webhook_url'])
    DISCORD_WEBHOOK_BOT = {
        "username": cfg.get("webhook_username"),
        "avatar_url": cfg.get("webhook_avatar_url")
    }
except Exception as ex:
    import traceback

    traceback.print_exc(ex)
    logger.error('Set up config.json! See https://github.com/aqur1n/SteamUpdates?tab=readme-ov-file#set-up-configjson')

if not exists('cache'):
    from os import mkdir
    mkdir('cache')
    
if exists('cache/branches.json'):
    with open('cache/branches.json', encoding = 'utf-8') as f:
        lst_update_bchs = loads(f.read())
else:
    lst_update_bchs = {}

def check_update_bch(cdn: CDNClient) -> None:
    depot_info = cdn.get_app_depot_info(APP_ID)

    for branch in depot_info['branches']:
        bch_data = depot_info['branches'][branch]
        bch_data['appid'] = APP_ID # for embeds

        if int(bch_data['timeupdated']) > lst_update_bchs.get(branch, 0):
            logger.info(f'Branch {branch} has updates, sending data...')

            try:
                if lst_update_bchs.get(branch, 0) != 0:
                    DISCORD_WEBHOOK.send(**DISCORD_WEBHOOK_BOT, embed = embed_updated_bch(branch, bch_data))
                else:
                    DISCORD_WEBHOOK.send(**DISCORD_WEBHOOK_BOT, embed = embed_created_bch(branch, bch_data))
            except Exception as ex:
                logger.error(f'There was an error when sending data to the webhook: {ex}')

            lst_update_bchs[branch] = int(bch_data['timeupdated'])

    with open('cache/branches.json', mode = 'w', encoding = 'utf-8') as f:
        f.write(dumps(lst_update_bchs))


if __name__ == '__main__':
    steam = SteamClient()
    steam.anonymous_login()

    logger.info('Logged in via anonymous. Getting started...')

    cdn = CDNClient(steam)

    while True:
        check_update_bch(cdn)

        sleep(120)
