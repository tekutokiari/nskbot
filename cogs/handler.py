import discord
from discord.ext import commands
import datetime

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.channel.id == 727961827937353768 or ctx.channel.id == 727620998395854878:
            return
        if hasattr(ctx.command, "on_error"):
            return
        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(color=discord.Color.gold(), description=':x: Invalid Command')
            await ctx.message.reply(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(color=discord.Color.gold(), description=f"You can use this command again in {round(error.retry_after, 2)} seconds.")
            await ctx.message.reply(embed=embed)
        elif isinstance(error, discord.Forbidden):
            embed = discord.Embed(color=discord.Color.gold(), description=":x: I don't have the permissions to do that.")
            await ctx.message.reply(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(color=discord.Color.gold(), description=':x: You do not meet the permissions required for this command.')
            await ctx.message.reply(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```Member not found!```")
            await ctx.message.reply(embed=embed)
        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```User not found!```")
            await ctx.message.reply(embed=embed)
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Role not found!```")
            await ctx.message.reply(embed=embed)
        elif isinstance(error, discord.NotFound):
            if ctx.command.qualified_name == 'unban':
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Error", value="```Unknown ban.```")
                await ctx.message.reply(embed=embed)
            else:
                raise error
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.qualified_name == 'kick':
                embed = discord.Embed(title="Incorect use of `kick` command!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}kick @user <reason>(optional)```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'ban':
                embed = discord.Embed(title="Incorect use of `ban` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}ban @user <reason>(optional)```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'unban':
                embed = discord.Embed(title="Incorect use of `unban` command!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix} unban <user>(id / name#discriminator) <reason>(optional)```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'purge':
                embed = discord.Embed(title="Incorect use of `purge` command!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}purge <amount>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'addcoins':
                embed = discord.Embed(title="Incorect use of `addcoins` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}addcoins @user <amount>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'removecoins':
                embed = discord.Embed(title="Incorect use of `removecoins` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}removecoins @user <amount>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'addshiny':
                embed = discord.Embed(title="Incorect use of `addshiny` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}addshiny @user <amount>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'removeshiny':
                embed = discord.Embed(title="Incorect use of `removeshiny` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}removeshiny @user <amount>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'coinflip':
                embed = discord.Embed(title="Incorect use of `coinflip` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}coinflip <amount> <choice>```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'deleterole':
                embed = discord.Embed(title="Incorect use of `deleterole` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}deleterole @role```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'addrole':
                embed = discord.Embed(title="Incorect use of `addrole` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}addrole @role @user```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'removerole':
                embed = discord.Embed(title="Incorect use of `removerole` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}removerole @role```")
            elif ctx.command.qualified_name == 'warn':
                embed = discord.Embed(title="Incorect use of `warn` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}warn @user <reason> (optional)```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'bugreport':
                embed = discord.Embed(title="Incorect use of `bugreport` command!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Correct use", value=f"```{ctx.prefix}bugreport <issue_ecountered>```")
                await ctx.message.reply(embed=embed)
            else:
                raise error
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'addcoins':
                embed = discord.Embed(title="Incorect use of `addcoins` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error", value="```Amount must be a number!```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'removecoins':
                embed = discord.Embed(title="Incorect use of `removecoins` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error", value="```Amount must be a number!```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'addshiny':
                embed = discord.Embed(title="Incorect use of `addshiny` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error", value="```Amount must be a number!```")
                await ctx.message.reply(embed=embed)
            elif ctx.command.qualified_name == 'removeshiny':
                embed = discord.Embed(title="Incorect use of `removeshiny` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error", value="```Amount must be a number!```")
                await ctx.message.reply(embed=embed)
            else:
                raise error
        else:
            raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
