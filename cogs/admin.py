import discord
from discord.ext import commands
import datetime
from firebase_admin import firestore
import firebase_admin
import time
import typing
import asyncio

db = firestore.client(firebase_admin._apps['maindb'])

async def timeouttask(ctx, user, time):
    await asyncio.sleep(time)
    role = discord.utils.get(ctx.guild.roles, id=728455626631675938)
    await user.remove_roles(role)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Admin"

    @commands.command(help="Kick someone from the server.", usage="kick @user <reason>(optional)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: typing.Optional[discord.Member], *, args=None):
        if user is None:
            embed = discord.Embed(title="Invalid use of `kick` comamnd!",timestamp=datetime.datetime.utcnow(),color=discord.Color.red())
            embed.add_field(name="Error:",value="User not specified!")
            return await ctx.send(embed=embed)
        _roles = []
        for x in user.roles:
            if not x.name == "@everyone":
                _roles.append(x.mention)
        roles = ", ".join(_roles)
        perms = []
        for x, y in user.permissions_in(ctx.channel):
            if y is True:
                perms.append(x)
        _permissions = ", ".join(perms)
        if user.guild_permissions.kick_members:
            await ctx.send("I can't kick him")
            await ctx.message.add_reaction("❌")
        else:
            embed = discord.Embed(title=f"{ctx.message.author} kicked {user}", timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            if args:
                await ctx.guild.kick(user, reason=args)
                embed.add_field(name="Reason: ", value=f"```{args}```", inline=False)
            else:
                await ctx.guild.kick(user)
            embed.add_field(name="Roles: ", value=f"{roles}", inline=False)
            embed.add_field(name="Permissions: ", value=f"```{_permissions}```")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(help="Ban someone from the server.", usage="ban @user <reason>(optional)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: typing.Optional[discord.Member], *, args=None):
        if user is None:
            embed = discord.Embed(title="Invalid use of `ban` comamnd!",timestamp=datetime.datetime.utcnow(),color=discord.Color.red())
            embed.add_field(name="Error:",value="User not specified!")
            return await ctx.send(embed=embed)
        _roles = []
        for x in user.roles:
            if not x.name == "@everyone":
                _roles.append(x.mention)
        roles = ", ".join(_roles)
        perms = []
        for x, y in user.permissions_in(ctx.channel):
            if y is True:
                perms.append(x)
        _permissions = ", ".join(perms)
        if user.guild_permissions.ban_members:
            await ctx.send("I can't ban this bitch")
            await ctx.message.add_reaction("❌")
        else:
            embed = discord.Embed(title=f"{ctx.message.author} banned {user}", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            if args:
                await ctx.guild.ban(user, reason=args)
                embed.add_field(name="Reason: ", value=f"```{args}```", inline=False)
            else:
                await ctx.guild.ban(user)
            embed.add_field(name="Roles: ", value=f"{roles}", inline=False)
            embed.add_field(name="Permissions: ", value=f"```{_permissions}```")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(help="Delete an amount of messages in the current channel.", usage="purge <amount>", aliases=["clear"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        if limit >= 999:
            embed = discord.Embed(title="Incorect use of `purge` command!", timestamp=datetime.datetime.utcnow(), color=discord.Colour.red())
            embed.add_field(name="Error:", value="```Too many messages!```")
            return await ctx.send(embed=embed)
        await ctx.channel.purge(limit=limit+1)

    @commands.command(help="Create a new role with optional optional color, hoist and if it can be mentionable or not.",
        usage="createrole <color>(optional->hex) <hoist>(optional->True/False) <mentioable>(optional->True/False) <name>",
        aliases=["newrole"]
    )
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def createrole(self, ctx, color: typing.Optional[discord.Color] = None, hoist: typing.Optional[bool] = False, mentionable: typing.Optional[bool] = False, *, name: str = None):
        if name is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```Name the role first!```")
            return await ctx.send(embed=embed)
        if color:
            role = await ctx.guild.create_role(name=name, color=color, hoist=hoist, mentionable=mentionable)
        else:
            role = await ctx.guild.create_role(name=name, hoist=hoist, mentionable=mentionable)
        embed = discord.Embed(color=discord.Color.gold(), description=f'Successfully created role {role.mention}.')
        await ctx.send(embed=embed)

    @commands.command(help="Delete a role.", usage="deleterole @role")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def deleterole(self, ctx, role: discord.Role):
        await role.delete()
        embed = discord.Embed(color=discord.Color.gold(), description=f"Role deleted: **{role.name}**.")
        await ctx.send(embed=embed)
        
    @commands.command(help="Change your nickname.", usage="nick <nickname>", aliases=["nickname", "nick"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def changenick(self, ctx, *, nickname: str = None):
        user = ctx.author
        if nickname is None:
            await ctx.author.edit(nick=ctx.author.name)
            await ctx.message.add_reaction('✅')
        elif len(nickname) > 32:
            await ctx.message.add_reaction('❌')
        else:
            role = discord.utils.get(user.roles, name="〈 📜 〉")
            if role is None:
                embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Error", value="You need the〈 📜 〉role to change your nickname.")
                return await ctx.send(embed=embed)
            await ctx.author.edit(nick=nickname)
            await ctx.message.add_reaction('✅')

    @commands.command(help="Unban someone from the server.", usage="unban <user>(id / name#discriminator) <reason>(optional)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, args: str=None):
        if user is None:
            embed = discord.Embed(title="Invalid use of `unban` comamnd!",timestamp=datetime.datetime.utcnow(),color=discord.Color.red())
            embed.add_field(name="Error:",value="User not specified!")
            return await ctx.send(embed=embed)
        embed = discord.Embed(title=f"{ctx.message.author} unbanned {user}", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        if args:
            await ctx.guild.unban(user, reason=args)
            embed.add_field(name="Reason: ", value=f"{args}")
        else:
            await ctx.guild.unban(user)
        await ctx.send(embed=embed)

    @commands.command(help="Warn a user about an action they did.", usage="warn @user <reason>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.User, *, args: str = None):
        if not user:
            embed = discord.Embed(title="Incorect use of `warn` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error:", value="```Member not found!```")
            await ctx.send(embed=embed)
        warns = db.collection("warnings").document(f"{user.id}").get()
        if not warns.exists:
            createwarndb = db.collection("warnings").document(f"{user.id}")
            createwarndb.set({
                'nrw': 1,
                'warns': {
                    "1": args,
                    '1t': round(time.time() * 1000)
                }
            }, merge=True)
        else:
            nrwarns = warns.to_dict()['nrw']
            db.collection("warnings").document(f"{user.id}").set({
                'nrw': nrwarns+1,
                'warns': {
                    str(nrwarns+1): args,
                    str(nrwarns+1) + 't': round(time.time() * 1000)
                }
            }, merge=True)
        warns = db.collection("warnings").document(f"{user.id}").get()
        nrwarns = warns.to_dict()['nrw']
        embed = discord.Embed(title=f"Warned {user.name}!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
        embed.add_field(name="Warn number: ", value=f"```{nrwarns}```")
        embed.add_field(name="Warn Reason: ", value=f"```{args}```")
        embed.add_field(name="Warned By: ", value=f"```{ctx.author.name}#{ctx.author.discriminator}```")
        await ctx.send(embed=embed)

    @commands.command(help="Permanently mute someone.", usage="mute @user <reason>(optional)")
    @commands.has_guild_permissions(manage_messages=True)
    async def mute(self, ctx, user: typing.Optional[discord.Member], *, args: typing.Optional[str]):
        if not user or user is None:
            embed = discord.Embed(title="Incorect use of `mute` command!", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Member not found!```")
            await ctx.send(embed=embed)
        elif user.guild_permissions.manage_messages:
            embed = discord.Embed(title="Incorect use of `mute` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Member has MANAGE_MESSAGES permission!```")
            return await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, id=728455626631675938)
            await user.add_roles(role)
            embed = discord.Embed(color=discord.Color.gold(), description=f"```{ctx.author} just permanently muted {user}```")
            embed.add_field(name="Reason:", value=f"```{args}```")
            await ctx.send(embed=embed)

    @commands.command(help="Unmute someone.", usage="unmute @user")
    @commands.has_guild_permissions(manage_messages=True)
    async def unmute(self, ctx, user: typing.Optional[discord.Member]):
        if not user or user is None:
            embed = discord.Embed(title="Incorect use of `unmute` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Member not found!```")
            await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, id=728455626631675938)
            await user.remove_roles(role)
            embed = discord.Embed(color=discord.Color.gold(), description=f"{ctx.author} just unmuted {user}")
            await ctx.send(embed=embed)

    @commands.command(help="Temporarily mute someone.", usage="mute @user <time> (ex: 10s/5m/1h) <reason>(optional)")
    @commands.has_guild_permissions(manage_messages=True)
    async def tempmute(self, ctx, user: typing.Optional[discord.Member], time=None, reason: str = None):
        if not user or user is None:
            embed = discord.Embed(title="Incorect use of `tempmute` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Member not found!```")
            return await ctx.send(embed=embed)
        elif user.guild_permissions.manage_messages:
            embed = discord.Embed(title="Incorect use of `tempmute` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Member has MANAGE_MESSAGES permission!```")
            return await ctx.send(embed=embed)
        elif not time or time is None:
            embed = discord.Embed(title="Incorect use of `tempmute` command!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Mute time not specified!```")
            return await ctx.send(embed=embed)
        else:
            if reason is None or not reason:
                reason = "No reason"
            def convert_time_to_seconds(time):  #a function that converts the mute time according to how the command author specified
                time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "S": 1, "M": 60, "H": 3600}
                try:
                    x = time_convert[time[-1]]
                except Exception as error:
                    if isinstance(error, KeyError):
                        x = 0
                if x:
                    try:
                        return int(time[:-1]) * time_convert[time[-1]]
                    except:
                        return time
                else:
                    return False
            if not convert_time_to_seconds(time):
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of time (ex: 10s, 10m, 10h, 10d, 10w).')
                return await ctx.send(embed=embed)
            time = convert_time_to_seconds(time)
            muteexpire = int(datetime.datetime.utcnow().timestamp()) + time
            mexpire = round(muteexpire * 1000)
            finalexpire = datetime.datetime.fromtimestamp(mexpire/1000.0, tz=datetime.timezone.utc)
            role = discord.utils.get(ctx.guild.roles, id=728455626631675938)
            await user.add_roles(role)
            embed = discord.Embed(title=f"{ctx.author} temporarily muted {user}", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason:", value=f"```{reason}```")
            embed.add_field(name="Mute duration: ", value=f"```{time} seconds```")
            embed.add_field(name="Mute expires on: ", value=f"```{finalexpire}```")
            await ctx.send(embed=embed)
            self.bot.loop.create_task(timeouttask(ctx, user, time))

    @commands.command(help="Lock a text channel. Only permissions for @everyone are affected.", usage="lock #channel(optional - if no channel is mentioned then the channel where the command was invoked will be locked)")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        embed = discord.Embed(color=discord.Color.gold(), description='```Channel has been locked.```')
        await channel.send(embed=embed)

    @commands.command(help="Unlock a text channel. Only permissions for @everyone are affected.", usage="unlock #channel(optional - if no channel is mentioned then the channel where the command was invoked will have the send_messages permission overridden)")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel =  ctx.channel
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        embed = discord.Embed(color=discord.Color.gold(), description=f'```Channel has been unlocked.```')
        await channel.send(embed=embed)

    @commands.command(
        help="Lock all text and voice channels (except the ones that are invisible to the default role). Only permissions for @everyone are affected. ***Note that there will be a certain delay between channels because of ratelimits.***",
        usage="lockdown"
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def lockdown(self, ctx):
        embed = discord.Embed(color=discord.Color.gold(), description='```Server lockdown.```')
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            if perms.send_messages is (None or True):
                perms.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                await channel.send(embed=embed)
                await asyncio.sleep(1.5)
            else:
                pass
        for channel in ctx.guild.voice_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            if perms.connect is (None or True):
                perms.connect = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                await asyncio.sleep(1.5)
            else:
                pass

    @commands.command(
        help="Unlock the text/voice channels. Only permissions for @everyone are affected (it may be destructive to permissions set for private channels). ***Note that there will be a certain delay between channels because of ratelimits.***",
        usage="lockdownend"
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def lockdownend(self, ctx):
        embed = discord.Embed(color=discord.Color.gold(), description='```Lockdown ended.```')
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            await channel.send(embed=embed)
            await asyncio.sleep(1.5)
        for channel in ctx.guild.voice_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.connect = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            await asyncio.sleep(1.5)

def setup(bot):
    bot.add_cog(Admin(bot))
