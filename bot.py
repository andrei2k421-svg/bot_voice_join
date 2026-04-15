import discord
from discord.ext import commands
import requests

# ===== CONFIG =====
import os
TOKEN = os.getenv("TOKEN")
OWNER_ID = 281850118682968066   # your user ID
TARGET_USER_ID = 773853422062796840  # user1 ID

PUSHOVER_TOKEN = "az47ei1t29p79un87d5cvha3ntk1p6"
PUSHOVER_USER = "ubhhucqsbwk4at77r5fhx1e5mibdec"

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Only track target user
    if member.id != TARGET_USER_ID:
        return

    # Detect JOIN
    if before.channel is None and after.channel is not None:
        channel_name = after.channel.name
        message = f"🔔 {member.name} joined voice channel: {channel_name}"

        print(f"Event detected: {message}")

        # ===== 1. Send Discord DM =====
        try:
            owner = await bot.fetch_user(OWNER_ID)
            await owner.send(message)
            print("✅ DM sent")
        except Exception as e:
            print(f"❌ Failed to send DM: {e}")

        # ===== 2. Send Pushover notification =====
        try:
            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": message
                }
            )
            if response.status_code == 200:
                print("✅ Pushover notification sent")
            else:
                print(f"❌ Pushover failed: {response.text}")
        except Exception as e:
            print(f"❌ Pushover error: {e}")

bot.run(TOKEN)