import discord
import asyncio
from colorama import init, Fore, Style
from messagecopier import MessageCloner

# Initialize terminal colors
init(autoreset=True)

print(f"{Fore.RED}🩸 Blood Cloner V1 - by Envyonix{Style.RESET_ALL}\n")

# Inputs
token = input("Enter your bot token:\n> ").strip()
source_guild_id = int(input("Enter source guild ID:\n> ").strip())
target_guild_id = int(input("Enter target guild ID:\n> ").strip())
num_channels = int(input("How many channels do you want to clone?\n> ").strip())

source_channels = []
for i in range(num_channels):
    channel_id = int(input(f"Enter source channel ID #{i+1}:\n> ").strip())
    source_channels.append(channel_id)

# Discord client setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[INFO] Logged in as {Fore.GREEN}{client.user}{Style.RESET_ALL}")
    source_guild = client.get_guild(source_guild_id)
    target_guild = client.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        print(f"[ERROR] Could not find one or both guilds. Check IDs and permissions.")
        await client.close()
        return

    await MessageCloner.clone_multiple_channels(client, source_channels, target_guild)
    print(f"[SUCCESS] All channels cloned!")
    await asyncio.sleep(2)
    await client.close()

client.run(token)
