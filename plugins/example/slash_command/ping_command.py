from discord import app_commands,Interaction
from discord.ext import commands

from typing import Optional


class ping_command(commands.Cog):
    def __init__(self,bot):
        self.app: Optional[commands.Bot]=bot

    @app_commands.command(name='ping',description='check bot latency')
    async def ping(self,interaction:Interaction) -> None:
        await interaction.response.defer(thinking=True)
        ping = self.app.latency * 1000
        await interaction.followup.send(f"Pong! `{(round(ping,2))} ms`")


