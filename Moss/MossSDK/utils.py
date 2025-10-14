import json
import discord
from pathlib import Path


class utils():
    @staticmethod
    def json_to_embed(json_data) -> discord.Embed:
        """

        :param json_data: path or json string
        :return:
        """

        try:
            json.loads(json_data)
        except json.decoder.JSONDecodeError:
            with open(json_data) as json_file:
                data = json.load(json_file)

