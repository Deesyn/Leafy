import discord
def _add_intents(config: dict, intents: discord.Intents.default()) -> None:
    intents.guilds = config['discord']['intents'].get('guilds', False)
    intents.guild_members = config['discord']['intents'].get('guild_members', False)
    intents.guild_bans = config['discord']['intents'].get('guild_bans', False)
    intents.guild_emojis_and_stickers = config['discord']['intents'].get('guild_emojis_and_stickers', False)
    intents.guild_integrations = config['discord']['intents'].get('guild_integrations', False)
    intents.guild_webhooks = config['discord']['intents'].get('guild_webhooks', False)
    intents.guild_invites = config['discord']['intents'].get('guild_invites', False)
    intents.guild_voice_states = config['discord']['intents'].get('guild_voice_states', False)
    intents.guild_presences = config['discord']['intents'].get('guild_presences', False)
    intents.guild_messages = config['discord']['intents'].get('guild_messages', False)
    intents.guild_message_reactions = config['discord']['intents'].get('guild_message_reactions', False)
    intents.guild_message_typing = config['discord']['intents'].get('guild_message_typing', False)
    intents.guild_polls = config['discord']['intents'].get('guild_polls', False)
    intents.guild_scheduled_events = config['discord']['intents'].get('guild_scheduled_events', False)

    # direct message
    intents.dm_messages = config['discord']['intents'].get('dm_messages', False)
    intents.dm_reactions = config['discord']['intents'].get('dm_reactions', False)
    intents.dm_typing = config['discord']['intents'].get('dm_typing', False)

    # global-level
    intents.message_content = config['discord']['intents'].get('message_content', False)
    intents.presences = config['discord']['intents'].get('presences', False)
    intents.reactions = config['discord']['intents'].get('reactions', False)
    intents.typing = config['discord']['intents'].get('typing', False)
    intents.voice_states = config['discord']['intents'].get('voice_states', False)
    intents.members = config['discord']['intents'].get('members', False)

    # automod
    intents.auto_moderation_configuration = config['discord']['intents'].get(
        'auto_moderation_configuration', False
    )
    intents.auto_moderation_execution = config['discord']['intents'].get(
        'auto_moderation_execution', False
    )