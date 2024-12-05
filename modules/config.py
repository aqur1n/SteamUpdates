
from json import loads
from typing import Union

from discord import SyncWebhook


class Config:
    def __init__(self, cfg: dict):
        self.__app_id: int = cfg['app_id']
        self.__branch_pings: dict[str, list[int]] = cfg.get("branch_pings", {})
        self.__branches_whitelist: Union[list[str], None] = cfg.get("branches_whitelist")

        d = cfg['discord_webhook']
        self.__dw_url: str = d['url']
        self.__dw_kwargs: dict[str, Union[str, None]] = {
            "username": d.get("username"),
            "avatar_url": d.get("avatar_url")
        }
        self.__dw: SyncWebhook = SyncWebhook.from_url(self.__dw_url)

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        with open(path, encoding = 'utf-8') as file:
            return cls(loads(file.read()))
        
    @property
    def app_id(self) -> int:
        return self.__app_id
    
    @property
    def discord_webhook_url(self) -> int:
        return self.__dw_url
    
    @property
    def discord_webhook_kwargs(self) -> int:
        return self.__dw_kwargs
    
    @property
    def webhook(self) -> SyncWebhook:
        return self.__dw
    
    def get_branch_pings(self, branch: str) -> list[int]:
        return self.__branch_pings.get(branch, [])
    
    @property
    def branches_whitelist(self) -> Union[list[str], None]:
        return self.__branches_whitelist
