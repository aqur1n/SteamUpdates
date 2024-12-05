
from json import dumps, loads
import logging
from time import time
from discord import Colour, Embed, EmbedField
from steam.client import SteamClient, EResult

from .config import Config


logger = logging.getLogger(__name__)

def format_bch_name(raw_name: str, bch_data: dict) -> str:
    name = ""

    if bch_data.get('lcsrequired') == '1':
        name += "📁 "
    if bch_data.get('pwdrequired') == '1':
        name += "🔒"

    return name + raw_name

def embed_updated_bch(raw_name: str, bch_data: dict) -> Embed: 
    time_updated = int(bch_data.get('timeupdated', time()))
    return Embed(
        colour = Colour.from_rgb(255, 140, 0),
        title = f'Branch {format_bch_name(raw_name, bch_data)} has been updated',
        description = bch_data.get('description'),
        fields = [
            EmbedField(name = "Build ID", value = bch_data.get('buildid', 'None'), inline = True),
            EmbedField(name = "Time updated", value = f'<t:{time_updated}:F> <t:{time_updated}:R>', inline = True),
            EmbedField(name = "More info", value = f'[steamdb.info](https://steamdb.info/app/{bch_data["appid"]}/depots/?branch={raw_name})')
        ]
    )

def embed_created_bch(raw_name: str, bch_data: dict) -> Embed: 
    embed = embed_updated_bch(raw_name, bch_data)
    embed.title = f'Branch {format_bch_name(raw_name, bch_data)} has been created/updated'
    embed.colour = Colour.from_rgb(0, 200, 0)
    return embed

class SteamUpdater:
    def __init__(self, client: SteamClient, cfg: Config) -> None:
        self.client = client
        self.cfg = cfg
        self.branches_cache = {}

    def branches_cache_from_file(self, path: str = 'cache/branches.json') -> None:
        with open('cache/branches.json', encoding = 'utf-8') as f:
            self.branches_cache = loads(f.read())

    def branches_cache_to_file(self, path: str = 'cache/branches.json') -> None:
        with open('cache/branches.json', mode = 'w', encoding = 'utf-8') as f:
            f.write(dumps(self.branches_cache))

    def login(self) -> None:
        if self.client.logged_on:
            return
        
        l = self.client.anonymous_login()
        if l == EResult.OK:
            logger.info('Logged in via anonymous. Getting started...')
        else:
            logger.error(f'Connection error to anonymous, response: {l}')
            quit(1)

    def send_embed(self, embed: Embed, content: str = None) -> None:
        self.cfg.webhook.send(content, **self.cfg.discord_webhook_kwargs, embed = embed)

    def check_branches(self) -> None:
        depot_info = self.client.get_product_info([self.cfg.app_id], timeout = 60)['apps'][self.cfg.app_id]['depots']
        logger.debug(f"Data of the branches of the application {self.cfg.app_id} has been received.")

        for branch in depot_info['branches']:
            if self.cfg.branches_whitelist is not None and branch not in self.cfg.branches_whitelist:
                continue

            bch_data = depot_info['branches'][branch]
            bch_data['appid'] = self.cfg.app_id # for embeds

            if int(bch_data['timeupdated']) > self.branches_cache.get(branch, 0):
                logger.info(f'Branch {branch} has updates, sending data...')

                try:
                    if self.branches_cache.get(branch, 0) != 0:
                        self.send_embed(
                            embed_updated_bch(branch, bch_data),
                            content = ', '.join(self.cfg.get_branch_pings(branch))
                        )
                    else:
                        self.send_embed(
                            embed_created_bch(branch, bch_data),
                            content = ', '.join(self.cfg.get_branch_pings(branch))
                        )

                    logger.info('The data was sent successfully')
                    self.branches_cache[branch] = int(bch_data['timeupdated'])
                except Exception as ex:
                    logger.error(f'There was an error when sending data to the webhook: {ex}')

        self.branches_cache_to_file()