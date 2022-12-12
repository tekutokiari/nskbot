import discord
from discord.ext import commands
import asyncio
import random
from firebase_admin import firestore
import datetime
import typing
import firebase_admin

db = firestore.client(firebase_admin._apps['maindb'])

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Fun"

    @commands.command(aliases=['parrot', 'mimic', 'repeat'], help="make the bot say what you want.", usage="say <text>")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def say(self, ctx, *, mimic=None):
        if mimic is None:
            return await ctx.message.delete()
        await ctx.message.delete()
        await ctx.send(mimic)

    @commands.command(help="Make your message be extremely sarcastic or overenthusiastic.", usage="clapify <text>")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clapify(self, ctx, *, text):
        if ctx.channel.id != 728299872947667106:
            return
        message = ''
        for x in text[-len(text):-1]:
            message += f'**{x}**'
            message += " :clap: "
        message += f'**{text[-1]}**'
        await ctx.send(message)

    @commands.command(help='Encrypt your message to annoy someone (for long texts Satan has a spot waiting just for you).', usage="spoilify <text>")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def spoilify(self, ctx, *, text):
        if ctx.channel.id != 728299872947667106:
            return
        await ctx.message.delete()
        message = f'**{ctx.message.author}** - '
        for x in text:
            message += f'||{x}||'
        await ctx.send(message)

    @commands.command(help="convert text into corresponding emojis", usage="emojify <text>")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        if ctx.channel.id != 728299872947667106:
            return
        message = ''
        numbers = {
            '0': ':zero:', '1': ':one:', '2': ':two:', '3': ':three:', '4': ':four:', '5': ':five:', '6': ':six:', '7': ':seven:', '8': ':eight:', '9': ':nine:'
        }
        for x in text:
            if x.isalpha():
                message += f':regional_indicator_{x.lower()}:'
            elif x.isdigit():
                message += numbers[x]
            elif x == ' ':
                message += '     '
            else:
                message += x
        await ctx.send(message)

    @commands.command(help="You literally don't have anything better to do if you're using this command, am I right?", usage="pun")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pun(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        pun = random.choice(list(open('./text files/puns.txt', encoding='utf8')))
        await ctx.send(pun)

    @commands.command(help="Roast someone or yourself.", usage="roast @user (optional)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roast(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        roast = random.choice(list(open('./text files/roast.txt', encoding='utf8')))
        await ctx.send(roast)

    @commands.command(aliases=['fortunecookie', 'fortune'], help="Yes, fortune cookies, let's see what you get.", usage="fookie")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def fookie(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        fortune = random.choice(list(open('./text files/fookies.txt', encoding='utf8')))
        embed = discord.Embed(color=discord.Color.gold(), description=f':fortune_cookie: {fortune}', title=str(ctx.message.author))
        await ctx.send(embed=embed)

    @commands.command(help="Play a game of russian roulette.", usage="russianroulette @user(s) (max 5 players mentioned)", aliases=["rr", "russianr", "rroullete"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def russianroulette(self, ctx, users: commands.Greedy[discord.Member]):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.author in users:
            users.remove(ctx.author)
        if users == []:
            return await ctx.send("***You can't play by yourself.***")
        if len(users) > 5:
            return await ctx.send(f"***Only 6 players can play, not {len(users)+1}!***")
        users.append(ctx.author)
        random.shuffle(users)
        rounds = []
        for x in range(0, len(users)):
            rounds.append(0)
        rounds[0] = 1
        random.shuffle(rounds)
        user_shot = random.choices(users, weights=rounds, k=1)
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), title="Preparing...")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        embed.title = "6 rounds have been fired..."
        embed.description = "**Results:**\n\n"
        await message.edit(embed=embed)
        await asyncio.sleep(2)
        users.remove(user_shot[0])
        for x in range(0, len(users)):
            embed.description += f"**{users[x].name}** *empty shot*   :gun:\n"
            await message.edit(embed=embed)
            await asyncio.sleep(2)
        embed.description += f"**{user_shot[0].name}** :fire: :gun:"
        await message.edit(embed=embed)

    @commands.command(aliases=['rps'], help="duel with someone in the ultimate battle", usage="rps <choice> @user")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rockpaperscissors(self, ctx, choice: str=None, member: discord.Member=None):
        if ctx.channel.id != 728299872947667106:
            return
        choice_list = ['rock', 'paper', 'scissors']
        embed = discord.Embed(title='**Rock**-**Paper**-**Scissors**', color=discord.Color.gold())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/750789031134232758/rps.png')
        if not choice:
            embed.description = 'Choose your weapon first.'
            embed.set_footer(icon_url=self.bot.user.avatar_url, text='"rock"/"paper"/"scissors"')
            embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
            return await ctx.send(embed=embed)
        elif choice.lower() not in choice_list:
            embed.description = 'Not a valid choice. Choose between **rock**-**paper**-**scissors**.'
            embed.set_footer(icon_url=self.bot.user.avatar_url, text="Let's keep it basic and not play with lasers and guns.")
            embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
            return await ctx.send(embed=embed)
        if not member:
            embed.description = 'Mention someone to duel with.'
            embed.set_footer(icon_url=self.bot.user.avatar_url, text='You could try and play with yourself irl tho (and no, not that way).')
            embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
            return await ctx.send(embed=embed)
        if member.bot:
            embed.description = "You can't play with bots. They'll destroy you."
            embed.set_footer(icon_url=self.bot.user.avatar_url, text="Or ignore you. We're busy things.")
            embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
            return await ctx.send(embed=embed)
        await ctx.message.delete()
        embed.description = f'{ctx.message.author.mention} **provoked you to the ultimate duel, make your choice.**'
        embed.set_author(icon_url=member.avatar_url, name=member)
        embed.set_footer(icon_url=self.bot.user.avatar_url, text='Respond with "rock"/"paper"/"scissors" to the duel.')
        await ctx.send(embed=embed)
        await ctx.send(member.mention)
        def check(x):
            return x.author == member and x.channel == ctx.message.channel
        try:
            member_choice = await self.bot.wait_for('message', check=check, timeout=20)
            a = choice.lower()
            b = member_choice.content.lower()
            if b not in choice_list:
                embed.description = 'Not a valid choice. Choose between **rock**-**paper**-**scissors** next time.'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text="Let's keep it basic and not play with lasers and guns.")
                embed.set_author(icon_url=member.avatar_url, name=member)
            if (a == 'rock' and b == 'scissors'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':mountain: **Rock wins!**\n**Congrats** {ctx.message.author.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{member} was defetead.')
            elif (b == 'rock' and a == 'scissors'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':mountain: **Rock wins!**\n**Congrats** {member.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{ctx.message.author} was defetead.')
            elif (a == 'paper' and b == 'rock'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':page_facing_up: **Paper wins!**\n**Congrats** {ctx.message.author.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{member} was defetead.')
            elif (b == 'paper' and a == 'rock'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':page_facing_up: **Paper wins!**\n**Congrats** {member.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{ctx.message.author} was defetead.')
            elif (a == 'scissors' and b == 'paper'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':scissors: **Scissors win!**\n**Congrats** {ctx.message.author.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{member} was defetead.')
            elif (b == 'paper' and a == 'scissors'):
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = f':scissors: **Scissors win!**\n**Congrats** {member.mention}!'
                embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'{ctx.message.author} was defetead.')
            elif a == b:
                embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
                embed.description = ":crossed_swords: **It's a tie!**"
                embed.set_footer(icon_url=self.bot.user.avatar_url, text='What a fight.')
        except asyncio.TimeoutError:
            embed.set_author(icon_url=self.bot.user.avatar_url, name='End of the battle')
            embed.description = f"{member.mention} chose silence..."
            embed.set_footer(icon_url=self.bot.user.avatar_url, text='Better luck next time.')
            return await ctx.send(embed=embed)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dice', 'dices'], help="roll the dices", usage="roll")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        number = random.randint(1, 12)
        embed = discord.Embed(title=f'You rolled **__{number}__**', color=discord.Color.gold())
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/735245591872798810/dice.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['age', 'howmanydays'], help="Calculate your age in days.", usage="agedays `dd`/`mm`/`yyyy`")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def agedays(self, ctx, *, birthday):
        if ctx.channel.id != 728299872947667106:
            return
        date = birthday.split('/')
        if int(date[0]) > 31:
            return await ctx.send('Invalid date')
        elif int(date[1]) > 12:
            return await ctx.send('Invalid date')
        elif int(date[1]) == 2 and int(date[0]) > 28 and int(date[2])%4 != 0:
            return await ctx.send('Invalid date')
        elif (int(date[1]) == 4 or int(date[1]) == 6 or int(date[1]) == 9 or int(date[1]) == 11) and int(date[0]) > 30:
            return await ctx.send('Invalid date')
        date = datetime.datetime.strptime(birthday, '%d/%m/%Y')
        now = datetime.datetime.utcnow()
        age = now - date
        age = str(age)
        days = list(age.split(',', 1))
        embed = discord.Embed(description=days[0], color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def kleeb(self,ctx):
        await ctx.send('<@343911417075728385>')

def setup(bot):
    bot.add_cog(Fun(bot))
