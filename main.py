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

@bot.command(name="ask")
async def ask(ctx, *, question: str):
    try:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel is None:
            await ctx.send("❌ I couldn't find the target channel.")
            return

        # Post anonymous question without mentioning anyone
        await target_channel.send(f"**Anonymous question:**\n{question}")

        # Optionally DM the owner that a new question came in
        #owner = await bot.fetch_user(OWNER_USER_ID)
        #await owner.send(
        #    f"New anonymous question submitted by {ctx.author}:\n\n{question}"
        #)

        # Confirm to the user
        await ctx.send("✅ Your question has been sent!", delete_after=10)

    except Exception as e:
        print(f"Error: {e}")
        
# Start the bot
keep_alive()
bot.run(token)
