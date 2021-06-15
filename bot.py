from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
# CONSTANTS
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot('+') #Discord Bot (Subclass of Discord.Client())

@bot.command()
async def load_cog(ctx,name):
    bot.load_extension(f'modules.{name}')
    
@bot.command()
async def unload_cog(ctx,name):
    bot.unload_extension(f'modules.{name}')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,CommandNotFound):
        await ctx.send(':doge_gun: Speak something I understand! :doge_gun:')

for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')
bot.run(TOKEN)