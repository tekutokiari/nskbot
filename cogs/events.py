import time
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord import File
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import random
from firebase_admin import firestore
import firebase_admin
import datetime
import asyncio

db = firestore.client(firebase_admin._apps['maindb'])
db2 = firestore.client(firebase_admin._apps['extra-database'])

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coin_block.start()
        self.mhg.start()

    @tasks.loop(hours=12, reconnect=True)
    async def mhg(self):
        ch = await self.bot.fetch_channel(727620998395854878)
        await ch.send("<@251389420584960002> MHG")

    @tasks.loop(hours=2, reconnect=True)
    async def coin_block(self):
        try:
            channel = await self.bot.fetch_channel(727620998395854878)
            embed = discord.Embed(title="A wild Coin Block has spawned", description="**Quick! Press the reaction button and collect coins** <:coin:845012771594043412>", timestamp=datetime.datetime.utcnow())
            embed.set_author(name="NS Kingdom", icon_url="https://cdn.discordapp.com/icons/727575735316775073/a_d9095627f2e6ffd0ef65f9ae7966f60a.gif?size=1024")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/842074906204045315/842150379210801182/image0.png")
            message = await channel.send(embed=embed)
            _id = message.id
            await message.add_reaction("<:emoji_37:843862766715404359>")
            await asyncio.sleep(10)
            message = await channel.fetch_message(_id)
        except Exception as error:
            error = getattr(error, "original", error)
            if isinstance(error, discord.Forbidden):
                pass
            else:
                raise error
        try:
            for reaction in message.reactions:
                try:
                    if reaction.emoji.id == 843862766715404359:
                        amount_list = []
                        users = await reaction.users().flatten()
                        users = users[1:]
                        for user in users:
                            amount = random.randint(50, 75)
                            amount_list.append(amount)
                            try:
                                balance = db.collection("balance").document(f"{user.id}").get().to_dict()["coins"]
                                db.collection("balance").document(f"{user.id}").set({
                                    "coins": balance + amount
                                }, merge=True)
                            except Exception as error:
                                if isinstance(error, KeyError):
                                    db.collection("balance").document(f"{user.id}").set({
                                        "coins": amount
                                    }, merge=True)
                                elif isinstance(error, TypeError):
                                    db.collection("balance").document(f"{user.id}").set({
                                        "coins": amount
                                    }, merge=True)
                                else:
                                    raise error
                except Exception as error:
                    if isinstance(error,AttributeError):
                        pass
            embed.description = "Event expired"
            embed.add_field(name="Users", value="\n".join(list(map(lambda x: x.name, users))))
            embed.add_field(name="Coins", value="\n".join(list(map(lambda x: str(x), amount_list))))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/842074906204045315/842150382926692379/image0.png")
            await message.edit(embed=embed)
        except Exception as error:
            error = getattr(error, "original", error)
            if isinstance(error, discord.HTTPException):
                await message.delete()
            elif isinstance(error, discord.Forbidden):
                pass
            elif isinstance(error, UnboundLocalError):
                pass
            else:
                raise error

    @staticmethod
    def add_shiny(member: discord.Member):
        shinybalance = db.collection("shiny").document(f"{member.id}").get()
        if not shinybalance.exists:
            createbalance = db.collection("balance").document(f"{member.id}")
            createbalance.set({
                'coins': 0
            }, merge=True)
            createshiny = db.collection("shiny").document(f"{member.id}")
            createshiny.set({
                'shiny': 1
            }, merge=True)
        else:
            bal = shinybalance.to_dict()['shiny']
            db.collection("shiny").document(f"{member.id}").update({"shiny": bal+1})

    @staticmethod
    def fetch_balance(member: discord.Member):
        balance = db.collection("balance").document(f"{member.id}").get()
        shinybalance = db.collection("shiny").document(f"{member.id}").get()
        coins = balance.to_dict()['coins']
        shiny = shinybalance.to_dict()['shiny']
        currency = list()
        currency.append(coins)
        currency.append(shiny)
        return currency

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.content.lower() == "ban":
                await message.channel.send("http://giphygifs.s3.amazonaws.com/media/qPD4yGsrc0pdm/giphy.gif")
            if message.content.lower() == "creeper":
                await message.channel.send("https://media.discordapp.net/attachments/534053698880667689/637682779177615371/creeper.gif")
            guess_channel = await self.bot.fetch_channel(805687713587527770)
            if not message.author.bot:
                thread_pool = ThreadPoolExecutor(max_workers=2)
                def probability(chance: float):
                    return random.random() < chance
                shiny_badge = discord.utils.get(message.guild.roles, id=735576193990000741)
                if shiny_badge in message.author.roles:
                    prob = probability(float(1/1000))
                else:
                    prob = probability(float(1/3000))
                if prob:
                    partial_shiny = partial(self.add_shiny, message.author)
                    partial_fetch_bal = partial(self.fetch_balance, message.author)
                    await self.bot.loop.run_in_executor(thread_pool, partial_shiny)
                    currency = await self.bot.loop.run_in_executor(thread_pool, partial_fetch_bal)
                    await message.add_reaction('<:1_shiny_rupee:755974674927845456>')
                else:
                    pass
            nr = db.collection('royalguess').document('rguess').get().to_dict()['guessnr']
            if message.channel.id == 780118905431392277:
                if message.content.startswith("[Suggestion]") or message.content.startswith("[suggestion]"):
                    await message.add_reaction('<:upvote:840441611359485973>')
                    await message.add_reaction('<:downvote:840441625184567326>')
                else:
                    if message.author.guild_permissions.manage_roles:
                        if message.content.startswith("[Suggestion]") or message.content.startswith("[suggestion]"):
                            await message.add_reaction('<:upvote:780093470983192606>')
                            await message.add_reaction('<:downvote:780093496899010570>')
                    else:
                        await message.delete()
            if not message.channel.id == guess_channel.id:
                pass
            else:
                if message.author.bot == False:
                    try:
                        try:
                            a = int(message.content)
                            lastguess = db2.collection('royalguess').document(f'{message.author.id}').get()
                            then = lastguess.to_dict()['lastguess']
                            today = int(round(time.time()*1000))
                            todaydate = datetime.datetime.fromtimestamp(today/1e3)
                            thendate = datetime.datetime.fromtimestamp(900+then/1e3)
                            timeleft = abs(todaydate-thendate)
                            seconds = timeleft.seconds
                            minutes = (seconds % 3600) // 60
                            seconds = seconds % 60
                            if todaydate < thendate:
                                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                                embed.description = f"You can guess again in **{str(minutes) + 'm ' + str(seconds) + 's'}**"
                                return await message.channel.send(embed=embed)
                        except Exception as error:
                            if isinstance(error,TypeError):
                                db2.collection('royalguess').document(f'{message.author.id}').set({'lastguess': int(time.time()*1000)},merge=True)
                            elif isinstance(error,ValueError):
                                await message.delete()
                            else:
                                raise error
                        try_count = db.collection('royalguess').document('rguess').get().to_dict()['amountguess']
                        if int(message.content) == nr:
                            try_count = 0
                            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                            embed.set_author(name="Royal Guess", icon_url=guess_channel.guild.icon_url)
                            embed.description = f"{message.author.mention} guessed the number and got 1000<:coin:845012771594043412>! It was: `{nr}`"
                            await guess_channel.send(embed=embed)
                            db.collection('royalguess').document('rguess').set({u'guessnr': random.randint(1,1000)},merge=True)
                            try:
                                bal = db.collection('balance').document(f'{message.author.id}').get().to_dict()['coins']
                                db.collection('balance').document(f'{message.author.id}').set({'coins': bal + 1000},merge=True)
                                if bal is None:
                                    raise TypeError
                            except TypeError:
                                db.collection('balance').document(f'{message.author.id}').set({'coins': 1000},merge=True)
                            new_embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                            new_embed.set_author(name="Royal Guess", icon_url=guess_channel.guild.icon_url)
                            new_embed.description = "***Generating number...***"
                            new_nr_message = await guess_channel.send(embed=new_embed)
                            await asyncio.sleep(3)
                            new_embed.description = "Random number generated you may start guessing!"
                            await new_nr_message.edit(embed=new_embed)
                        elif int(message.content) < nr:
                            if try_count == 2:
                                await guess_channel.send("***Go higher...***")
                                db.collection('royalguess').document('rguess').set({"amountguess": 0}, merge=True)
                            else:
                                db.collection('royalguess').document('rguess').set({"amountguess": try_count + 1}, merge=True)
                        elif int(message.content) > nr:
                            if try_count == 2:
                                await guess_channel.send("***Go lower...***")
                                db.collection('royalguess').document('rguess').set({"amountguess": 0}, merge=True)
                            else:
                                db.collection('royalguess').document('rguess').set({"amountguess": try_count + 1}, merge=True)
                        db2.collection('royalguess').document(f'{message.author.id}').set({'lastguess': int(time.time()*1000)},merge=True)
                    except Exception as error:
                        raise error
        except Exception as error:
            error = getattr(error, "original", error)
            if isinstance(error, discord.HTTPException):
                pass
            elif isinstance(error, discord.Forbidden):
                pass
            elif isinstance(error, UnboundLocalError):
                pass
            else:
                raise error

    @staticmethod
    def get_avatar(buffer: BytesIO, resize: tuple):
        buffer.seek(0)
        avatar_image = Image.open(buffer)
        avatar_image = avatar_image.resize(resize)
        return avatar_image

    @staticmethod
    def welcome_image(avatar: Image, member):
        with Image.open('./images/welcomebg.png') as background:
            buffer_output = BytesIO()
            background.paste(avatar, (25, 100))
            font = ImageFont.truetype("./fonts/sfcartoonisthand.ttf", 70)
            w, h = 1442, 439
            draw = ImageDraw.Draw(background)
            draw.text((350, 100), "Welcome to NS KINGDOM", fill="#000000", font=font)
            draw.text((w/2-100, h/2+40), f"{member}", fill="#000000", font=font, anchor="mm")
            background.save(buffer_output, format='PNG')
            buffer_output.seek(0)
        return buffer_output

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.fetch_channel(727620998395854878)
        rules_ch = await self.bot.fetch_channel(728298727323861002)

        avatar_buffer = BytesIO()
        member_avatar = member.avatar_url_as(format='png', size=256)
        await member_avatar.save(avatar_buffer)

        thread_pool = ThreadPoolExecutor(max_workers=2)

        avatar_partial = partial(self.get_avatar, avatar_buffer, (256, 256))
        avatar_image = await self.bot.loop.run_in_executor(thread_pool, avatar_partial)
        background_partial = partial(self.welcome_image, avatar_image, member)
        final_buffer = await self.bot.loop.run_in_executor(thread_pool, background_partial)
        _file = File(filename=f"welcome+{member}.png", fp=final_buffer)

        await channel.send(f"**> Welcome {member.mention}!**")
        await member.send(file=_file)
        await member.send(f"Hey {member.mention}!\n***Welcome to NS KINGDOM!***\n\n__Let’s Get Started!__\n\nRead {rules_ch.mention}!\n(Remember to scroll all the way to the top!)\n\nEnjoy your stay at NSK!")

        thread_pool.shutdown(wait=True)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        member = discord.utils.get(after.guild.members, id=after.id)
        if len(before.roles) < len(after.roles):
            role = [x for x in after.roles if x not in before.roles]
            if role[0].id == 838879110595084339:
                star_badge = discord.utils.get(after.guild.roles, id=732765784333615165)
                await member.add_roles(star_badge)
            elif role[0].id == 727634503962591345:
                try:
                    balance = db.collection("balance").document(f"{member.id}").get().to_dict()["coins"]
                    db.collection("balance").document(f"{member.id}").set({
                        "coins": balance + 2500
                    }, merge=True)
                except Exception as error:
                    if isinstance(error, TypeError):
                        db.collection("balance").document(f"{member.id}").set({
                            "coins": 2500
                        }, merge=True)
                    elif isinstance(error, KeyError):
                        db.collection("balance").document(f"{member.id}").set({
                            "coins": 2500
                        }, merge=True)
                    else:
                        raise error
                dm = await member.create_dm()
                embed =discord.Embed(color=discord.Color.gold(), title="Thank you for boosting our server!", timestamp=datetime.datetime.utcnow())
                embed.set_author(name="NS Kingdom", icon_url=after.guild.icon_url)
                embed.description = "You have been awarded 2500 <:coin:845012771594043412>."
                await dm.send(embed=embed)
            badge_ids = [833119201371226162, 833127117092814898, 833128418845392926, 833308095710887957, 838905788276801566, 838905871492579389, 838905938710757418, 838905940014792706]
            member_role_ids = list(map(lambda x: x.id, after.roles))
            badge_count = 1
            for _id in member_role_ids:
                if _id in badge_ids:
                    badge_count += 1
            if badge_count == len(badge_ids):
                shiny_badge = discord.utils.get(after.guild.roles, id=735576193990000741)
                await member.add_roles(shiny_badge)
        else:
            pass

def setup(bot):
    bot.add_cog(Events(bot))
