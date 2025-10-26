import re
import discord
from datetime import timedelta
from typing import Optional
from discord.ext import commands
from discord import app_commands

class mute_command(commands.Cog):
    def __init__(self,bot):
        self.app: Optional[commands.Bot] =  bot
    def _time_parser(self,Input):
        pairs = [[int(num),char] for num,char in re.findall(r"(\d+)([a-zA-Z])", Input)]
        full_time = 0
        for time,sub in pairs:
            if sub == 's':
                full_time += time
            if sub == 'min':
                full_time += time*60
            if sub == 'h':
                full_time += time*60*60
            if sub == 'd':
                full_time += time*60*60*24
        return timedelta(full_time)

    @app_commands.command(name='f-mute',description='mute user')
    @app_commands.describe(user='chose a user',until='only supports: s/m/h/d')
    async def mute(self,interaction: discord.Interaction,until:str,user: discord.Member):
        await interaction.response.defer(thinking=True)
        user_permission = interaction.user.guild_permissions
        if user_permission.mute_members:
            try:
                await user.timeout(self._time_parser(Input=until))
            except Exception as e:
                await interaction.followup.send(f"``⚠️`` An error has occurred")
        else:
            await interaction.followup.send(f"``❌`` You need permission ``mute_members`` to use this command!")