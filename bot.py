import discord
from discord.ext import commands
from datetime import datetime
import sys

if len(sys.argv) < 2
    print("Usage: python bot.py <token_file>")
    sys.exit(1)

token_file = sys.argv[1]

with open(token_file, "r") as f:
   TOKEN = f.read().strip()

CLAIMER_ROLE = "Claimer"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

claimed_requests = {}  # message_id -> user_id

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def request(ctx, date: str, time: str):
    """
    Usage: !request YYYY-MM-DD HH:MM
    """
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        await ctx.send("Invalid date format. Use YYYY-MM-DD HH:MM")
        return

    msg = await ctx.send(
        f"📅 **Request Available**\n"
        f"Time: {dt.strftime('%B %d, %Y at %I:%M %p')}\n"
        f"React with ✅ to claim"
    )
    await msg.add_reaction("✅")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message

    if str(reaction.emoji) != "✅":
        return

    if message.id in claimed_requests:
        return

    guild = message.guild
    member = guild.get_member(user.id)

    if not any(role.name == CLAIMER_ROLE for role in member.roles):
        await reaction.remove(user)
        return

    claimed_requests[message.id] = user.id
    await message.edit(content=message.content + f"\n\n✅ *Claimed by {user.mention}*")

bot.run(TOKEN)
