import discord
from discord.ext import commands
import os
import traceback
import io
import textwrap
from contextlib import redirect_stdout
import config
import helpcmd
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('serviceaccount.json')
dapp = firebase_admin.initialize_app(cred, name="maindb")

cred2 = credentials.Certificate('serviceaccount2.json')
dapp2 = firebase_admin.initialize_app(cred2, name="extra-database")

intents = discord.Intents.all()
mentions = discord.AllowedMentions(everyone=False)

"""
def get_prefix(bot, message):
    result = guild_collection.find_one({"_id": message.guild.id})
    prefix = result["prefix"]
    return commands.when_mentioned_or(prefix)(bot, message)
"""

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

bot = Bot (
    command_prefix="!",
    case_insensitive=True,
    help_command=helpcmd.help_object,
    allowed_mentions=mentions,
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.watching, name='NS KINGDOM'),
    status=discord.Status.online,
)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - {bot.user.id}\ndiscord.py: v{discord.__version__}\n')

def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

def is_owner(ctx):
    return ctx.author.id in [465138950223167499, 465138950223167499,449555448010375201,449555448010375201,450883984600072193,396002772568506369]

@bot.command(aliases=['eval', 'ev'], hidden=True)
@commands.is_owner()
async def _eval(ctx, *, body):
    _last_result = None
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': _last_result
    }
    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, " ")}'
    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    func = env['func']
    ret = None
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass
    if ret is None:
        if value:
            await ctx.send(f'```py\n{value}\n```')
        else:
            _last_result = ret
            await ctx.send(f'```py\n{value}{ret}\n```')

@bot.command(hidden=True)
@commands.check(is_owner)
async def sudo(ctx, user: discord.Member, *, command):
    message = ctx.message
    message.author = user
    message.content = ctx.prefix + command
    await bot.process_commands(message)

bot.run(config.token)
