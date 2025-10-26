import discord

class create_ticket_button(discord.ui.View):
    @discord.ui.button(label='Tạo ticket',style=discord.ButtonStyle.green)
    async def create_ticket(self,interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
