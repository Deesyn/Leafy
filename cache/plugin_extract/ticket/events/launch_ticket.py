import discord
from discord.ext import commands
from typing import Optional
from Swit.sdk.utils.config import config
from plugins.ticket.ui.button.create_ticket_button import create_ticket_button
class launch_ticket(commands.Cog):
    def __init__(self, bot):
        self.bot: Optional[commands.Bot] = bot
    @commands.Cog.listener()
    async def on_ready(self):
        await self.launch_ticket()
    async def launch_ticket(self):
        config_data = config.read(config_name='config.yml')

        title_data = config_data['embed']['launch_ticket_embed']['title']
        description_data = config_data['embed']['launch_ticket_embed']['description']
        color_data = config_data['embed']['launch_ticket_embed']['color']
        channel_id = config_data['ticket']['launch_at']['channel_id']
        embed = discord.Embed(
            title=str(title_data),
            description=str(description_data),
            color=color_data
        )
        view = create_ticket_button()
        channel = self.bot.get_channel(channel_id)
        await channel.send(embed=embed, view=view)