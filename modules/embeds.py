
from time import time

from discord import Embed, EmbedField, Colour


COLOUR_CREATED_BCH = Colour.from_rgb(0, 200, 0)
COLOUR_UPDATED_BCH = Colour.from_rgb(255, 140, 0)

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
        colour = COLOUR_UPDATED_BCH,
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
    embed.colour = COLOUR_CREATED_BCH
    return embed
