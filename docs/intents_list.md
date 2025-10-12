# Discord Intents Overview<br>
# Intents control which events your bot will receive from the Discord Gateway.<br>
# Enabling unnecessary intents can waste resources or require extra permissions.<br>

# Guild Intents<br>
**guilds**:
    Receive basic server information such as name, icon, roles, and channels.<br>

**guild_members**:<br>
    Receive member-related events such as join, leave, or role updates.<br>
    ⚠️ Privileged intent — must be enabled in the Developer Portal.<br>

**guild_bans**:<br>
    Receive events when a user is banned or unbanned from the guild.<br>

**guild_emojis_and_stickers**:<br>
    Receive updates when emojis or stickers are created, removed, or modified.<br>

**guild_integrations**:<br>
    Receive events related to integrations (e.g., Twitch, YouTube, etc.).<br>

**guild_webhooks**:<br>
    Receive events when webhooks are created, updated, or deleted.<br>

**guild_invites**:<br>
    Receive events when invites are created or deleted.<br>

**guild_voice_states**:<br>
    Receive updates about members connecting, disconnecting, or muting in voice channels.<br>

**guild_presences**:<br>
    Receive updates about members’ online status, activities, or custom statuses.<br>
    ⚠️ Privileged intent — must be enabled in the Developer Portal.<br>

**guild_messages**:<br>
    Receive messages sent in guild text channels.<br>

**guild_message_reactions**:<br>
    Receive reaction add/remove events in guild channels.<br>

**guild_message_typing**:<br>
    Receive typing start events in guild channels.<br>

**guild_polls**:<br>
    Receive updates about Discord’s new poll system (if supported).<br>

**guild_scheduled_events**:<br>
    Receive events related to scheduled events (creation, start, end, deletion).<br>

# Direct Message (DM) Intents<br>
**dm_messages**:<br>
    Receive direct messages sent to the bot.<br>

**dm_reactions**:<br>
    Receive reaction add/remove events in DMs.<br>

**dm_typing**:<br>
    Receive typing start events in DMs.<br>

# Global / General Intents<br>
**message_content**:<br>
    Allow access to the actual message text content.<br>
    ⚠️ Privileged intent — must be enabled in the Developer Portal.<br>

**presences**:<br>
    Receive global presence (status/activity) updates for users.<br>
    ⚠️ Privileged intent — must be enabled in the Developer Portal.<br>

**reactions**:<br>
    Receive global reaction events (messages, emojis, etc.).<br>

**typing**:<br>
    Receive typing start events globally.<br>

**voice_states**:<br>
    Receive global updates for users joining or leaving voice channels.<br>

**members**:<br>
    Receive global updates about members joining, leaving, or being updated.<br>
    ⚠️ Privileged intent — must be enabled in the Developer Portal.<br>

# Auto Moderation Intents<br>
**auto_moderation_configuration**:<br>
    Receive updates when auto-moderation rules are created, deleted, or modified.<br>

**auto_moderation_execution**:<br>
    Receive notifications when an auto-moderation rule is triggered.<br>
