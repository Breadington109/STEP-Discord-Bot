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
TARGET_CHANNEL_ID = 1388228345812226109  # Channel where questions are sent
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

    # Only handle DMs
    if message.guild is None:
        try:
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            if target_channel is None:
                await message.channel.send("❌ I couldn't find the anonymous channel.")
                return

            # Post anonymously
            await target_channel.send(f"**Anonymous question:**\n{message.content}")

            # Optionally notify the owner privately
            #owner = await bot.fetch_user(OWNER_USER_ID)
            #await owner.send(
            #    f"New anonymous question submitted by {message.author}:\n\n{message.content}"
            #)

            # Confirm to the user
            await message.channel.send("✅ Your anonymous question has been posted!")

        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("❌ Something went wrong posting your question.")
    else:
        # Optionally, inform users not to use the bot in servers
        await message.channel.send(
            "❌ Please DM me your question so it stays anonymous."
        )
        
# Start the bot
keep_alive()
bot.run(token)
