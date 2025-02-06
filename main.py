# -*- coding: utf-8 -*-

import logging
from time import sleep
from traceback import print_exc
from os.path import exists, dirname, realpath
from os import chdir

from steam.client import SteamClient
from gevent import Timeout

from modules.config import Config
from modules.steam import SteamUpdater


if __name__ == '__main__':
    logging.basicConfig(
        level = logging.INFO,
        format = r'[%(asctime)s] [%(levelname)s]  %(message)s',
    )
    logger = logging.getLogger(__name__)

    chdir(dirname(realpath(__file__)))
    if not exists('cache'):
        from os import mkdir
        mkdir('cache')

    if not exists('config.json'):
        logger.error('Set up config.json! See https://github.com/aqur1n/SteamUpdates?tab=readme-ov-file#set-up-configjson')
    cfg = Config.from_file('config.json')

    client = SteamUpdater(None, cfg)
    client.branches_cache_from_file()
    while True:
        try:
            client.login()

            logger.debug("Checking for branch updates...")
            client.check_branches()
        except Timeout:
            logger.warning('The time has expired when receiving the data, a second attempt...')
        except Exception as ex:
            print_exc()
        else:
            sleep(300)
