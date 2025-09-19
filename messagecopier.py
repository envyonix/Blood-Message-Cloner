import discord
import asyncio

class MessageCloner:
    @staticmethod
    async def clone_single_channel(client, source_channel_id, target_guild):
        source_channel = client.get_channel(source_channel_id)
        if not source_channel:
            print(f"[ERROR] Source channel {source_channel_id} not found.")
            return

        # Check if target channel exists
        target_channel = discord.utils.get(target_guild.text_channels, name=source_channel.name)
        if not target_channel:
            # Copy permissions
            overwrites = {}
            for role, perms in source_channel.overwrites.items():
                target_role = discord.utils.get(target_guild.roles, name=role.name)
                if target_role:
                    overwrites[target_role] = perms
            # Create target channel
            target_channel = await target_guild.create_text_channel(
                name=source_channel.name,
                overwrites=overwrites,
                topic=source_channel.topic,
                slowmode_delay=source_channel.slowmode_delay,
                nsfw=source_channel.nsfw
            )
            print(f"[INFO] Created target channel #{target_channel.name}")

        # Create a webhook for sending messages
        webhooks = await target_channel.webhooks()
        webhook = webhooks[0] if webhooks else await target_channel.create_webhook(name="BloodCloner Webhook")

        # Clone messages
        async for message in source_channel.history(limit=None, oldest_first=True):
            if message.author == client.user:
                continue

            files = [discord.File(await att.read(), filename=att.filename) for att in message.attachments]
            embeds = message.embeds

            await webhook.send(
                content=message.content or None,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                embeds=embeds if embeds else None,
                files=files if files else None,
                allowed_mentions=discord.AllowedMentions.none()
            )

            # Copy reactions
            for reaction in message.reactions:
                try:
                    last_msg = await target_channel.history(limit=1, oldest_first=False).next()
                    for _ in range(reaction.count):
                        await last_msg.add_reaction(reaction.emoji)
                except Exception:
                    pass
            await asyncio.sleep(0.5)

        print(f"[SUCCESS] Finished cloning channel #{source_channel.name}")

    @staticmethod
    async def clone_multiple_channels(client, source_channel_ids, target_guild):
        for ch_id in source_channel_ids:
            await MessageCloner.clone_single_channel(client, ch_id, target_guild)
        print("[INFO] All channels processed.")
