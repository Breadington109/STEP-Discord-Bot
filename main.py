from flask import Flask
from threading import Thread
import os
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()

import discord
from discord.ext import commands

# Replace these with your values
token = os.getenv("TOKEN")
TARGET_CHANNEL_ID = 1386730467730129077  # Channel where questions are asked
OWNER_USER_ID = 692429491003326524     # Your Discord user ID

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.messages = True
intents.dm_messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Only monitor the specific channel
    if message.channel.id == TARGET_CHANNEL_ID:
        try:
            # Send DM to the owner
            owner = await bot.fetch_user(OWNER_USER_ID)
            await owner.send(
                f"New message from {message.author} in #{message.channel}:\n\n{message.content}"
            )

            # Delete the original message
            await message.delete()

            # Confirm in channel
            await message.channel.send(f"✅ Your question has been sent!", delete_after=5)

        except Exception as e:
            print(f"Error: {e}")

# Start the bot
keep_alive()
bot.run(token)
