import discord
from discord.ext import commands
from firebase_admin import firestore
import datetime
import time
import random
import typing
import firebase_admin

db = firestore.client(firebase_admin._apps['maindb'])
db2 = firestore.client(firebase_admin._apps['extra-database'])

class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pet_urls = {
            'Bandana Dee': 'https://cdn.discordapp.com/attachments/839165416508883024/839165581491175474/Bandana_Dee.png',
            'Polari': 'https://cdn.discordapp.com/attachments/839165416508883024/839167546384187452/Polari.png',
            'Thwimp': 'https://cdn.discordapp.com/attachments/839165416508883024/839167367707492362/Thwimp.png',
            'Poochy': 'https://cdn.discordapp.com/attachments/839165416508883024/839165803793350686/Poochy.png',
            'Baby Yoshi': 'https://cdn.discordapp.com/attachments/839165416508883024/839168272083058718/Baby_Yoshi.png',
            'Plessie': 'https://cdn.discordapp.com/attachments/839165416508883024/839168498310840330/Plessie.png',
            'Korok': 'https://cdn.discordapp.com/attachments/839165416508883024/839168495957966878/Korok.png',
            'Boo Guy': 'https://cdn.discordapp.com/attachments/839165416508883024/839168383320457216/Boo_Guy.png',
            'K. K. Slider': 'https://cdn.discordapp.com/attachments/839165416508883024/839167843714072596/K._K._Slider.png',
            'Snom': 'https://cdn.discordapp.com/attachments/839165416508883024/839165430136045618/Snom.png',
            'Terrako': 'https://cdn.discordapp.com/attachments/839165416508883024/839169275251785768/Terrako.png',
            'Polterpup': 'https://cdn.discordapp.com/attachments/839165416508883024/839169274567589908/Polterpup.png',
            'Judd': 'https://cdn.discordapp.com/attachments/839165416508883024/839169272437014569/Judd.png',
            'Bobby': 'https://cdn.discordapp.com/attachments/839165416508883024/845750240459489310/Bobby.png',
            'Mew': 'https://cdn.discordapp.com/attachments/839165416508883024/839169273464225883/Mew.png'
        }

    alias = "Pets"

    @commands.command(aliases=['setupinv'], help="Use this command to set up your pet inventory.", usage="setup")
    async def setup(self, ctx):
        x = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if x is None:
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'cookbook':{},
                'cooldowns': {
                    'bath': 1,
                    'training': 1,
                    'hunt': 1,
                    'walk': 1,
                    'play': 1,
                    'ability': 1,
                    'switch': 1,
                },
                'dishes': {},
                'ingredients':{},
                'items': {
                    'Brush': False,
                    'Leash': False,
                    'Rubber Ball': False,
                    'Cook Book': False,
                },
                'pet': '',
                'pets': {},
                'setup': True
            },merge=True)
            return await ctx.message.reply("Inventory set!")
        else:
            return await ctx.message.reply("You can't setup your pet inventory again!")

    @commands.command(aliases=['ps','pshop'], help="The pet shop. See the available pets on the market.", usage="petshop")
    async def petshop(self, ctx):
        embed = discord.Embed(title="Welcome to NSK Pet Shop!", timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
        embed.add_field(name="1. Pet Capsule <:pet_capsule:838882986358997092>",value="<:arrow:752022451600228452> Capsule that gives you a random pet. \n Price: 2<:shiny_rupee:752022435296968746>",inline=False)
        embed.add_field(name="2. Rare Candy <:retard_rocky:916070708206002198>",value="<:arrow:752022451600228452> Gives 1100 XP to the current pet equipped \n Price: 3<:shiny_rupee:752022435296968746>",inline=False)
        embed.add_field(name="3. Lucky Egg <:lucky_egg:838559488683409459>",value="<:arrow:752022451600228452> Grants double XP for 10 activities \n Price: 1000<:coin:845012771594043412>",inline=False)
        embed.add_field(name="4. Rubber Ball <:rubber_ball:838559474838274048>",value="<:arrow:752022451600228452> Used to play with pets \n Price: 3500<:coin:845012771594043412>",inline=False)
        embed.add_field(name="5. Leash <:leash:839269905072652296>", value="<:arrow:752022451600228452> Used to take your pet out for a walk \n Price: 3500<:coin:845012771594043412>",inline=False)
        embed.add_field(name="6. Shampoo <:wash_bucket:839272321386545182>", value="<:arrow:752022451600228452> Used to wash your pet \n Price: 3500<:coin:845012771594043412>",inline=False)
        embed.add_field(name="7. Cook Book <:cook_book:840326571935399946>", value="<:arrow:752022451600228452> Remember all the dishes you cooked \n Price: 3500<:coin:845012771594043412>", inline=False)
        embed.add_field(name="8. Sheikah Slate <:sheikah_slate:842490321085923368>", value="<:arrow:752022451600228452> Choose a category of ingredients from which to hunt \n Price: 200<:coin:845012771594043412>", inline=False)
        await ctx.send(embed=embed)

    async def getpet(self, user):
        pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
        return pet

    @commands.command(aliases=['pequip'], help="Equip a pet from your inventory.", usage="petequip <pet>")
    async def petequip(self, ctx, *, args: typing.Optional[str]):
        if ctx.channel.id != 728299872947667106:
            return
        if args is None:
            return await ctx.message.reply("**Pet not found!**")
        pets_dict = {
            "bandana dee": ("Bandana Dee"),
            "bandana": ("Bandana Dee"),
            "dee": ("Bandana Dee"),
            "polari": ("Polari"),
            "thwimp": ("Thwimp"),
            "poochy": ("Poochy"),
            "snom": ("Snom"),
            "baby yoshi": ("Baby Yoshi"),
            "baby": ("Baby Yoshi"),
            "yoshi": ("Baby Yoshi"),
            "plessie":  ("Plessie"),
            "korok": ("Korok"),
            "boo": ("Boo Guy"),
            "guy": ("Boo Guy"),
            "boo guy": ("Boo Guy"),
            "K.": ("K. K. Slider"),
            "K. K.": ("K. K. Slider"),
            "slider": ("K. K. Slider"),
            "terrako": ("Terrako"),
            "polterpup": ("Polterpup"),
            "judd": ("Judd"),
            "bobby": ("Bobby"),
            "mew": ("Mew")
        }
        if pets_dict[args.lower()] == db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pet']:
            return await ctx.message.reply("**Pet already equipped!**")
        try:
            lastswitch = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['switch']
            then = lastswitch
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can switch your pet again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'switch': int(round(time.time() * 1000))
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {'switch':int(round(time.time() * 1000))}},merge=True)
            else:
                raise error
        owned = False
        for x in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
            if pets_dict[args.lower()] in x:
                owned = True
        if owned is False:
            return await ctx.message.reply("**Pet not owned!**")
        if args.lower() in pets_dict:
            db.collection('petinventory').document(f'{ctx.author.id}').set({'pet': pets_dict[args.lower()]},merge=True)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f"**{pets_dict[args.lower()]} equipped!**")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.pet_urls[pets_dict[args.lower()]])
            await ctx.send(embed=embed)
        else:
            return await ctx.message.reply("**Pet not found!**")

    @commands.command(aliases=['walk', 'pwalk'], help="Go to a walk with your pet.", usage="petwalk")
    async def petwalk(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        x = await self.getpet(ctx.author.id)
        if x is None or x == '':
            return await ctx.message.reply("You don't have any pet equipped!")
        if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Leash'] == False:
            return await ctx.message.reply("You don't have a `Leash`! Buy one from petshop to be able to walk your pet")
        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['XP']
        if type(xp) == str:
            return await ctx.send("You are at MAX LEVEL!")
        try:
            lastwalk = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['walk']
            then = lastwalk
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(3600+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can walk your pet again in **{str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'walk': int(round(time.time() * 1000))
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {'walk':int(round(time.time() * 1000))}},merge=True)
            else:
                raise error
        try:
            lucky_egg_amount = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()['items']["**3.** Lucky Egg"]
            xp_amount = 10
            if lucky_egg_amount - 1 == 0:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": lucky_egg_amount - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                xp_amount = 5
            else:
                raise error
        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['Level']
        if lvl == 1:
            xpcap = 300
        elif lvl == 2:
            xpcap= 700
        elif lvl == 3:
            xpcap= 1200
        elif lvl == 4:
            xpcap= 1500
        elif lvl == 5:
            xpcap= 1900
        if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Leash'] == True:
            if xp < xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    x: {
                        'XP': xp + xp_amount
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'You took {x} on a walk and it gained {xp_amount} XP!')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            if xp+5 >= xpcap and lvl != 5:
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Your pet leveled up! Current level: `{lvl+1}`')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets':{
                    x: {
                        'Level': lvl + 1,
                        'XP': 0
                    }}},merge=True)
            elif lvl == 5 and xp+xp_amount >= xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    x: {
                        'XP': 'MAX LEVEL'
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Level: MAX LEVEL')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)

    @commands.command(aliases=['wash', 'pwash'], help="Wash your pet.", usage="petwash")
    async def petwash(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        x = await self.getpet(ctx.author.id)
        if x is None or  x == '':
            return await ctx.message.reply("You don't have any pet equipped!")
        if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Shampoo'] == False:
            return await ctx.message.reply("You don't have `Shampoo`! Buy one from petshop to be able to wash your pet")
        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['XP']
        if type(xp) == str:
            return await ctx.send("You are at MAX LEVEL!")
        try:
            lastwalk = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['bath']
            then = lastwalk
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can wash your pet again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'bath': int(round(time.time() * 1000))
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {'bath':int(round(time.time() * 1000))}},merge=True)
            else:
                raise error
        try:
            lucky_egg_amount = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()['items']["**3.** Lucky Egg"]
            xp_amount = 20
            if lucky_egg_amount - 1 == 0:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": lucky_egg_amount - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                xp_amount = 10
            else:
                raise error
        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['Level']
        if lvl == 1:
            xpcap = 300
        elif lvl == 2:
            xpcap= 700
        elif lvl == 3:
            xpcap= 1200
        elif lvl == 4:
            xpcap= 1500
        elif lvl == 5:
            xpcap= 1900
        if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Shampoo'] == True:
            if xp < xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    x: {
                        'XP': xp + xp_amount
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'You gave {x} a bath and it gained {xp_amount} XP!')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            if xp+10 >= xpcap and lvl != 5:
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Your pet leveled up! Current level: `{lvl+1}`')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets':{
                    x: {
                        'Level': lvl + 1,
                        'XP': 0
                    }}},merge=True)
            elif lvl == 5 and xp+xp_amount >= xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    x: {
                        'XP': 'MAX LEVEL'
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Level: MAX LEVEL')
                embed.set_thumbnail(url=self.pet_urls[x])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)

    @commands.command(aliases=['play', 'pplay'], help="Play with your pet.", usage="petplay")
    async def petplay(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        x = await self.getpet(ctx.author.id)
        if x is None or x == '':
            return await ctx.message.reply("You don't have any pet equipped!")
        if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Rubber Ball'] == True:
            pass
        else:
            return await ctx.message.reply("You don't have a `Rubber Ball`! Buy one from petshop to be able to play with your pet.")
        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['XP']
        if type(xp) == str:
            return await ctx.send("You are at MAX LEVEL!")
        try:
            lastwalk = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['play']
            then = lastwalk
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(1800+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can play with your pet again in **{str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'play': int(round(time.time() * 1000))
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {'play':int(round(time.time() * 1000))}},merge=True)
            else:
                raise error
        try:
            lucky_egg_amount = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()['items']["**3.** Lucky Egg"]
            xp_amount = 10
            if lucky_egg_amount - 1 == 0:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": lucky_egg_amount - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                xp_amount = 5
            else:
                raise error
        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['Level']
        if lvl == 1:
            xpcap = 300
        elif lvl == 2:
            xpcap= 700
        elif lvl == 3:
            xpcap= 1200
        elif lvl == 4:
            xpcap= 1500
        elif lvl == 5:
            xpcap= 1900
        if xp < xpcap:
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                x: {
                    'XP': xp + xp_amount
                }}},merge=True)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'You played with {x} and it gained {xp_amount} XP!')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if xp+5 >= xpcap and lvl != 5:
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'{x} leveled up! Current level: `{lvl+1}`')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets':{
                x: {
                    'Level': lvl + 1,
                    'XP': 0
                }}},merge=True)
        elif lvl == 5 and xp+xp_amount >= xpcap:
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                x: {
                    'XP': 'MAX LEVEL'
                }}},merge=True)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Level: MAX LEVEL')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['train','ptrain','pettrain','training'], help="Train your pet.", usage="pettraining")
    async def pettraining(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        x = await self.getpet(ctx.author.id)
        if x is None or x == '':
            return await ctx.message.reply("You don't have any pet equipped!")
        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['XP']
        if type(xp) == str:
            return await ctx.send("You are at MAX LEVEL!")
        try:
            lastwalk = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['training']
            then = lastwalk
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can train your pet again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'training': int(round(time.time() * 1000))
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {'training': int(round(time.time() * 1000))}},merge=True)
            else:
                raise error
        try:
            lucky_egg_amount = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()['items']["**3.** Lucky Egg"]
            xp_amount = 10
            if lucky_egg_amount - 1 == 0:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                    "items": {
                        "**3.** Lucky Egg": lucky_egg_amount - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                xp_amount = 5
            else:
                raise error
        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['Level']
        if lvl == 1:
            xpcap = 300
        elif lvl == 2:
            xpcap= 700
        elif lvl == 3:
            xpcap= 1200
        elif lvl == 4:
            xpcap= 1500
        elif lvl == 5:
            xpcap= 1900
        if xp < xpcap:
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                x: {
                    'XP': xp + xp_amount
                }}},merge=True)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'You trained {x} and it gained {xp_amount} XP!')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if xp+5 >= xpcap and lvl != 5:
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Your pet leveled up! Current level: `{lvl+1}`')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets':{
                x: {
                    'Level': lvl + 1,
                    'XP': 0
                }}},merge=True)
        elif lvl == 5 and xp+xp_amount >= xpcap:
            db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                x: {
                    'XP': 'MAX LEVEL'
                }}},merge=True)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Level: MAX LEVEL')
            embed.set_thumbnail(url=self.pet_urls[x])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)

    @commands.group(help="Buys an item from NSK Pet Shop.", usage="pbuy <item>", case_insensitive=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pbuy(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"**Please specify an item.**\n*ex: {ctx.prefix}buy <item>*", color=discord.Color.gold())
            embed.add_field(name="Available Items:", value="*Pet Capsule, Rare Candy, Lucky Egg, Rubber Ball, Leash, Shampoo, Cook Book*")
            await ctx.send(embed=embed)
    
    @pbuy.command(aliases=["pet", "capsule", "1", "petcapsule", "pet capsule" ,"pcapsule"], help="Buy a capsule containing a random pet.", usage="petcapsule")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _petcapsule(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        shinybal = db.collection('shiny').document(f'{ctx.author.id}').get().to_dict()['shiny']
        if shinybal < 2:
            return await ctx.message.reply("***You don't have enough shiny rupees.***")
        db.collection('shiny').document(f'{ctx.author.id}').set({'shiny': shinybal-2},merge=True)
        try:
            capsuleamount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['**1.** Pet Capsule']
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    '**1.** Pet Capsule': capsuleamount + 1
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**2**<:shiny_rupee:752022435296968746>")
            embed.add_field(name="You got: ",value="**Item:** Pet Capsule<:pet_capsule:838882986358997092>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        '**1.** Pet Capsule': 1 
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**2**<:shiny_rupee:752022435296968746>")
                embed.add_field(name="You got: ",value="**Item:** Pet Capsule<:pet_capsule:838882986358997092>")
                await ctx.send(embed=embed)

    @pbuy.command(aliases=["rare", "candy", "rare candy", "2"], help="Buy a rare candy that will give the pet 1100XP.", usage="rarecandy")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _rarecandy(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        shinybal = db.collection('shiny').document(f'{ctx.author.id}').get().to_dict()['shiny']
        if shinybal < 3:
            return await ctx.message.reply("***You don't have enough shiny rupees.***")
        db.collection('shiny').document(f'{ctx.author.id}').set({'shiny': shinybal-3},merge=True)
        try:
            sugaramount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['**2.** Rare Candy']
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    '**2.** Rare Candy': sugaramount + 1
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**3**<:shiny_rupee:752022435296968746>")
            embed.add_field(name="You got: ",value="**Item:** Rare Candy<:retard_rocky:916070708206002198>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        '**2.** Rare Candy': 1 
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**3**<:shiny_rupee:752022435296968746>")
                embed.add_field(name="You got: ",value="**Item:** Rare Candy<:nskcandy:838499072624951326>")
                await ctx.send(embed=embed)

    @pbuy.command(aliases=['lucky','egg','lucky egg', '3'], help="Grants double xp for the next 10 activities.", usage="luckyegg")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def luckyegg(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 1000:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-1000},merge=True)
        try:
            eggamount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['**3.** Lucky Egg']
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    '**3.** Lucky Egg': eggamount + 10
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**1000**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Lucky Egg<:lucky_egg:838559488683409459>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        '**3.** Lucky Egg': 10
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**1000**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Lucky Egg<:lucky_egg:838559488683409459>")
                await ctx.send(embed=embed)
    
    @pbuy.command(aliases=['rubber','ball','rubber ball', '4'], help="Buy a rubberball for your pet.", usage="rubberball")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def rubberball(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 3500:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-3500},merge=True)
        try:
            ball = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Rubber Ball']
            if ball == True:
                return await ctx.message.reply('**You already own a Rubber Ball!**')
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    'Rubber Ball': True
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Rubber Ball<:rubber_ball:838559474838274048>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        'Rubber Ball': True
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Rubber Ball<:rubber_ball:838559474838274048>")
                await ctx.send(embed=embed)

    @pbuy.command(help="Buy a leash for your pet.", usage="leash")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leash(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 3500:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-3500},merge=True)
        try:
            if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Leash'] == True:
                return await ctx.message.reply('**You already own a <:leash:839269905072652296>Leash!**')
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    'Leash': True
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Leash<:leash:839269905072652296>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        'Leash': True
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Leash<:leash:839269905072652296>")
                await ctx.send(embed=embed)

    @pbuy.command(help="Buy a shampoo bottle for your pet.", usage="shampoo")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def shampoo(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 3500:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-3500},merge=True)
        try:
            if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Shampoo'] == True:
                return await ctx.message.reply('**You already own <:wash_bucket:839272321386545182>Shampoo!**')
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    'Shampoo': True
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Shampoo<:wash_bucket:839272321386545182>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        'Shampoo': True
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Shampoo<:wash_bucket:839272321386545182>")
                await ctx.send(embed=embed)

    @pbuy.command(aliases=['cook', 'book','cook book'])
    @commands.cooldown(1,2,commands.BucketType.user)
    async def cookbook(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 3500:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-3500},merge=True)
        try:
            if db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Cook Book'] == True:
                return await ctx.message.reply('**You already own a <:cook_book:840326571935399946>Cook Book!**')
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    'Cook Book': True
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Cook Book<:cook_book:840326571935399946>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        'Cook Book': True
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**3500**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Cook Book<:cook_book:840326571935399946>")
                await ctx.send(embed=embed)

    @pbuy.command(aliases=["slate", "sheikah", "sslate"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _sheikahslate(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 200:
            return await ctx.message.reply("***You don't have enough coins.***")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-200},merge=True)
        try:
            sheikahs = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['**8.** Sheikah Slate']
            db.collection('petinventory').document(f'{ctx.author.id}').set({
                'items':{
                    '**8.** Sheikah Slate': sheikahs + 15
                }
            },merge=True)
            embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Price:', value="**200**<:coin:845012771594043412>")
            embed.add_field(name="You got: ",value="**Item:** Sheikah Slate<:sheikah_slate:842490321085923368>")
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'items':{
                        '**8.** Sheikah Slate': 15
                    }
                },merge=True)
                embed = discord.Embed(title="Transaction succesful!",timestamp = datetime.datetime.utcnow(),color=discord.Color.green())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.add_field(name='Price:', value="**200**<:coin:845012771594043412>")
                embed.add_field(name="You got: ",value="**Item:** Sheikah Slate<:sheikah_slate:842490321085923368>")
                await ctx.send(embed=embed)

    @commands.command(help="Set a category from which to receive ingredients from hunting. You can switch it anytime.", usage="sheikahslate <category> (BOTW, MARIO, AC, KIRBY)", aliases=["sheikah", "slate", "sslate"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def sheikahslate(self, ctx, *, category: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        if category is None:
            return await ctx.message.reply("***Choose a category between BOTW/MARIO/AC/KIRBY!***")
        category = category.lower()
        categories = {
            "botw": "BOTW",
            "mario": "MARIO",
            "ac": "AC",
            "kirby": "KIRBY"
        }
        try:
            category = categories[category]
        except KeyError:
            return await ctx.message.reply("***Not a valid category!***")
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        db.collection('petinventory').document(f'{ctx.author.id}').set({
            "sheikah": category
        }, merge=True)
        embed = discord.Embed(color=discord.Color.gold(), description=f"Succesfully set hunting category for Sheikah Slate to `{category}`", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(aliases=["petuse"], case_insensitive=True, help="Use an item from your pet inventory.", usage="puse <item>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def puse(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"**Please specify an item.**\n*ex: {ctx.prefix}use <item>*", color=discord.Color.gold())
            embed.add_field(name="Available Items:", value="*Pet Capsule, Rare Candy, Rubber Ball, Leash, Brush*")
            await ctx.send(embed=embed)

    @puse.command(aliases=['pet capsule','pet', 'capsule', '1'], help="Use  a pet capsule.", usage="puse petcapsule")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def petcapsule(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        try:
            authoritems = db.collection(u'petinventory').document(f'{ctx.author.id}').get().to_dict()
            if not "**1.** Pet Capsule" in authoritems['items'] or authoritems['items']['**1.** Pet Capsule'] < 1:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {
                    'Leash': False,
                    'Shampoo': False,
                    'Rubber Ball': False
                }},merge=True)
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        petrarity = ["common","rare","legendary"]
        commonpets = ['Bandana Dee', 'Polari', 'Thwimp', 'Poochy', 'Snom']
        rarepets = ['Baby Yoshi', 'Plessie', 'Korok', 'Boo Guy', 'K. K. Slider']
        legendarypets = ['Terrako', 'Polterpup', 'Judd', 'Bobby', 'Mew']
        choice = str(random.choices(petrarity, weights=[65,25,10],k=1))
        _choice = choice.replace("'", "").replace("[", "").replace("]", "")
        if _choice == "common":
            _commonpets = str(random.choices(commonpets, weights=[5,5,5,5,5], k = 1))
            __commonpets = _commonpets.replace('[', "").replace(']', "").replace("'", "")
            if __commonpets in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
                message = await ctx.message.reply('You got a pet you already had! The pet will be disenchanted into 1120 XP!')
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__commonpets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__commonpets]['XP']
                if lvl == 1:
                    xpcap = 300
                elif lvl == 2:
                    xpcap= 700
                elif lvl == 3:
                    xpcap= 1200
                elif lvl == 4:
                    xpcap= 1500 
                elif lvl == 5:
                    xpcap= 1900
                if xp + 1120 >= xpcap and lvl != 5 and lvl > 2:
                    amount = (1120 + xp) - xpcap
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'Level': lvl +1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                elif lvl == 1:
                    amount = 1120 - (xpcap - xp + 700)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'Level': lvl + 2,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 2:
                    amount = 1120 - (xpcap - xp)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'Level': lvl + 1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 > xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'XP': 'MAX LEVEL'
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 < xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __commonpets: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                petname = __commonpets
                if petname == 'Bandana Dee':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165581491175474/Bandana_Dee.png'
                elif petname == 'Polari':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167546384187452/Polari.png'
                elif petname == 'Thwimp':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167367707492362/Thwimp.png'
                elif petname == 'Poochy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165803793350686/Poochy.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839165430136045618/Snom.png'
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__commonpets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__commonpets]['XP']
                embed = discord.Embed(title=f"Your {__commonpets} stats!",timestamp=datetime.datetime.utcnow(),color=discord.Color.red())
                embed.add_field(name='Level: ',value=f'```{lvl}```')
                embed.add_field(name="XP: ", value=f'```{xp}```')
                embed.set_thumbnail(url=peturl)
                await message.edit(content=None,embed=embed)
            else:
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'pets': {
                        __commonpets:{
                            'Level': 1,
                            'XP': 0,
                            'equipped': False,
                            'rarity': 'Common'
                        }
                    }
                },merge=True)
                petname = __commonpets
                if petname == 'Bandana Dee':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165581491175474/Bandana_Dee.png'
                elif petname == 'Polari':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167546384187452/Polari.png'
                elif petname == 'Thwimp':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167367707492362/Thwimp.png'
                elif petname == 'Poochy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165803793350686/Poochy.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839165430136045618/Snom.png'
                embed=discord.Embed(title=f"You got a `{petname}`!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.set_image(url=peturl)
                embed.add_field(name="Level: ",value="```1```")
                embed.add_field(name="XP: ",value="```0```")
                embed.add_field(name='‍', value='‍')
                embed.add_field(name="Rarity: ", value="```Common```")
                embed.add_field(name="Special ability: ", value="```Unlocked at Max Level!```")
                embed.add_field(name='‍', value='‍')
                await ctx.send(embed=embed)
        elif _choice == 'rare':
            _rarepets = str(random.choices(rarepets, weights=[5,5,5,5,5], k = 1))
            __rarepets = _rarepets.replace('[', "").replace(']', "").replace("'", "")
            if __rarepets in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
                message = await ctx.message.reply('You got a pet you already had! The pet will be disenchanted into 1120 XP!')
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__rarepets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__rarepets]['XP']
                if lvl == 1:
                    xpcap = 300
                elif lvl == 2:
                    xpcap= 700
                elif lvl == 3:
                    xpcap= 1200
                elif lvl == 4:
                    xpcap= 1500
                elif lvl == 5:
                    xpcap= 1900
                if xp + 1120 >= xpcap and lvl != 5 and lvl > 2:
                    amount = (1120 + xp) - xpcap
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __rarepets: {
                                'Level': lvl +1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __rarepets: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                elif lvl == 1:
                    amount = 1120 - (xpcap - xp + 700)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __rarepets: {
                                'Level': lvl + 2,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 2:
                    amount = 1120 - (xpcap - xp)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __rarepets: {
                                'Level': lvl + 1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 > xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __rarepets: {
                                'XP': 'MAX LEVEL'
                            }
                        }
                    },merge=True)
                petname = __rarepets
                if petname == 'Baby Yoshi':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168272083058718/Baby_Yoshi.png'
                elif petname == 'Plessie':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168498310840330/Plessie.png'
                elif petname == 'Korok':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168495957966878/Korok.png'
                elif petname == 'Boo Guy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168383320457216/Boo_Guy.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839167843714072596/K._K._Slider.png'
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__rarepets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__rarepets]['XP']
                embed = discord.Embed(title=f"Your {__rarepets} stats!",timestamp=datetime.datetime.utcnow(),color=discord.Color.blue())
                embed.add_field(name='Level: ',value=lvl)
                embed.add_field(name="XP: ", value=xp)
                embed.set_thumbnail(url=peturl)
                await message.edit(content=None,embed=embed)
            else:
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'pets': {
                        __rarepets:{
                            'Level': 1,
                            'XP': 0,
                            'equipped': False,
                            'rarity': 'Rare'
                        }
                    }
                },merge=True)
                petname = __rarepets
                if petname == 'Baby Yoshi':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168272083058718/Baby_Yoshi.png'
                elif petname == 'Plessie':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168498310840330/Plessie.png'
                elif petname == 'Korok':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168495957966878/Korok.png'
                elif petname == 'Boo Guy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168383320457216/Boo_Guy.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839167843714072596/K._K._Slider.png'
                embed=discord.Embed(title=f"You got a `{petname}`!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.set_image(url=peturl)
                embed.add_field(name="Level: ",value="```1```")
                embed.add_field(name="XP: ",value="```0```")
                embed.add_field(name='‍', value='‍')
                embed.add_field(name="Rarity: ", value="```Rare```")
                embed.add_field(name="Special ability: ", value="```Unlocked at Max Level!```")
                embed.add_field(name='‍', value='‍')
                await ctx.send(embed=embed)
        elif _choice == 'legendary':
            _legendarypets = str(random.choices(legendarypets, weights=[5,5,5,5,5], k = 1))
            __legendarypets = _legendarypets.replace('[', "").replace(']', "").replace("'", "")
            if __legendarypets in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
                message = await ctx.message.reply('You got a pet you already had! The pet will be disenchanted into 1120 XP!')
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__legendarypets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__legendarypets]['XP']
                if lvl == 1:
                    xpcap = 300
                elif lvl == 2:
                    xpcap= 700
                elif lvl == 3:
                    xpcap= 1200
                elif lvl == 4:
                    xpcap= 1500
                elif lvl == 5:
                    xpcap= 1900
                if xp + 1120 >= xpcap and lvl != 5 and lvl > 2:
                    amount = (1120 + xp) - xpcap
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __legendarypets: {
                                'Level': lvl +1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __legendarypets: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                elif lvl == 1:
                    amount = 1120 - (xpcap - xp + 700)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __legendarypets: {
                                'Level': lvl + 2,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 2:
                    amount = 1120 - (xpcap - xp)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __legendarypets: {
                                'Level': lvl + 1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 > xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            __legendarypets: {
                                'XP': 'MAX LEVEL'
                            }
                        }
                    },merge=True)
                petname = __legendarypets
                if petname == 'Terrako':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169275251785768/Terrako.png'
                elif petname == 'Polterpup':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169274567589908/Polterpup.png'
                elif petname == 'Judd':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169272437014569/Judd.png'
                elif petname == 'Bobby':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/845750240459489310/Bobby.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839169273464225883/Mew.png'
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__legendarypets]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][__legendarypets]['XP']
                embed = discord.Embed(title=f"Your {__legendarypets} stats!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name='Level: ',value=lvl)
                embed.add_field(name="XP: ", value=xp)
                embed.set_thumbnail(url=peturl)
                await message.edit(content=None,embed=embed)
            else:
                db.collection('petinventory').document(f'{ctx.author.id}').set({
                    'pets': {
                        __legendarypets:{
                            'Level': 1,
                            'XP': 0,
                            'equipped': False,
                            'rarity': 'Legendary'
                        }
                    }
                },merge=True)
                petname = __legendarypets
                if petname == 'Terrako':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169275251785768/Terrako.png'
                elif petname == 'Polterpup':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169274567589908/Polterpup.png'
                elif petname == 'Judd':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169272437014569/Judd.png'
                elif petname == 'Bobby':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/845750240459489310/Bobby.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839169273464225883/Mew.png'
                embed=discord.Embed(title=f"You got a `{petname}`!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.set_image(url=peturl)
                embed.add_field(name="Level: ",value="```1```")
                embed.add_field(name="XP: ",value="```0```")
                embed.add_field(name='‍', value='‍')
                embed.add_field(name="Rarity: ", value="```Legendary```")
                embed.add_field(name="Special ability: ", value="```Unlocked at Max Level!```")
                embed.add_field(name='‍', value='‍')
                await ctx.send(embed=embed)
        capsuleamount = db.collection(u'petinventory').document(f"{ctx.author.id}").get().to_dict()['items']['**1.** Pet Capsule']
        db.collection(u'petinventory').document(f"{ctx.author.id}").set({u'items': {f'**1.** Pet Capsule': capsuleamount-1}}, merge=True)
        capsuleamount = db.collection(u'petinventory').document(f"{ctx.author.id}").get().to_dict()['items'][f'**1.** Pet Capsule']
        if capsuleamount == 0:
            db.collection(u'petinventory').document(f"{ctx.author.id}").set({u'items': {f'**1.** Pet Capsule': firestore.DELETE_FIELD}}, merge=True)
    
    @puse.command(aliases=['rare', 'candy', 'rare candy', '2'], help="Use a rarecandy.", usage="puse rarecandy")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def rarecandy(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        try:
            authoritems = db.collection(u'petinventory').document(f'{ctx.author.id}').get().to_dict()
            if not "**2.** Rare Candy" in authoritems['items'] or authoritems['items']['**2.** Rare Candy'] < 1:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {
                    'Leash': False,
                    'Shampoo': False,
                    'Rubber Ball': False
                }},merge=True)
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        pet = await self.getpet(ctx.author.id)
        if pet is None or pet == "":
            return await ctx.message.reply("You don't have any pet equipped!")
        message = await ctx.message.reply(f"```You sure you want to use the Rare Candy on {pet}? If not press the ❌ to cancel the command else press the ✅!```")
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        reaction,user = await self.bot.wait_for('reaction_add', check = lambda reaction,user: user == ctx.author and (reaction.emoji == '✅' or reaction.emoji == '❌'))
        if reaction.emoji == '✅':
            await message.delete()
            lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
            xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            if lvl == 1:
                xpcap = 300
            elif lvl == 2:
                xpcap= 700
            elif lvl == 3:
                xpcap= 1200
            elif lvl == 4:
                xpcap= 1500 
            elif lvl == 5:
                xpcap= 1900
            if xp == 'MAX LEVEL':
                return await ctx.message.reply(f"{pet} already has MAX XP!")
            else:
                if xp + 1120 >= xpcap and lvl != 5 and lvl > 2:
                    amount = (1120 + xp) - xpcap
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'Level': lvl +1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                elif lvl == 1:
                    amount = 1120 - (xpcap - xp + 700)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'Level': lvl + 2,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 2:
                    amount = 1120 - (xpcap - xp)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'Level': lvl + 1,
                                'XP': amount
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 >= xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'XP': 'MAX LEVEL'
                            }
                        }
                    },merge=True)
                elif lvl == 5 and xp + 1120 <= xpcap:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                        'pets':{
                            pet: {
                                'XP': xp + 1120
                            }
                        }
                    },merge=True)
                petname = pet
                if petname == 'Bandana Dee':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165581491175474/Bandana_Dee.png'
                elif petname == 'Polari':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167546384187452/Polari.png'
                elif petname == 'Thwimp':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167367707492362/Thwimp.png'
                elif petname == 'Poochy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165803793350686/Poochy.png'
                elif petname == 'Baby Yoshi':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168272083058718/Baby_Yoshi.png'
                elif petname == 'Plessie':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168498310840330/Plessie.png'
                elif petname == 'Korok':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168495957966878/Korok.png'
                elif petname == 'Boo Guy':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168383320457216/Boo_Guy.png'
                elif petname == 'K. K. Slider':
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839167843714072596/K._K._Slider.png'
                elif petname == 'Snom':
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839165430136045618/Snom.png'
                elif petname == 'Terrako':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169275251785768/Terrako.png'
                elif petname == 'Polterpup':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169274567589908/Polterpup.png'
                elif petname == 'Judd':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169272437014569/Judd.png'
                elif petname == 'Bobby':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/845750240459489310/Bobby.png'
                else:
                    peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839169273464225883/Mew.png'
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
                embed = discord.Embed(title=f"Your {pet} stats!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name='Level: ',value=f'```{lvl}```')
                embed.add_field(name="XP: ", value=f'```{xp}```')
                embed.set_thumbnail(url=peturl)
                await ctx.send(embed=embed)
            candyamount = db.collection(u'petinventory').document(f"{ctx.author.id}").get().to_dict()['items']['**2.** Rare Candy']
            db.collection(u'petinventory').document(f"{ctx.author.id}").set({u'items': {f'**2.** Rare Candy': candyamount-1}}, merge=True)
            candyamount = db.collection(u'petinventory').document(f"{ctx.author.id}").get().to_dict()['items'][f'**2.** Rare Candy']
            if candyamount == 0:
                db.collection(u'petinventory').document(f"{ctx.author.id}").set({u'items': {f'**2.** Rare Candy': firestore.DELETE_FIELD}}, merge=True)
        else:
            await message.edit(content='Command Canceled')
            await message.delete()

    @puse.command(help="Use your pet ability.", usage="puse ability")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def ability(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        activepet = await self.getpet(ctx.author.id)
        try:
            lastability = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['ability']
            then = lastability
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can use your pet's ability again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                'ability': int(round(time.time() * 1000)),
                }},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                    'ability':int(round(time.time() * 1000)),
                }},merge=True)
            else:
                raise error
        try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][activepet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][activepet]['XP']
        except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
        if activepet == 'Polterpup' and lvl == 5 and xp == "MAX LEVEL":
            crate = random.randint(1,3)
            try:
                inv = db.collection("items").document(f"{ctx.author.id}").get().to_dict()
                db.collection("items").document(f"{ctx.author.id}").set({u'items': 
                {
                    "**24.** Loot Crate": inv["items"]["**24.** Loot Crate"] + crate
                }}, merge=True)
                return await ctx.message.reply(f"**Your {activepet} used its ability and granted you {crate} Loot Crates!**")
            except Exception as error:
                if isinstance(error,TypeError):
                    db.collection(u'items').document(f'{ctx.author.id}').set({u'items': {"**24.** Loot Crate": crate}}, merge=True)
                    return await ctx.message.reply(f"**Your {activepet} used its ability and granted you {crate} Loot Crates!**")
                elif isinstance(error,KeyError):
                    db.collection(u'items').document(f'{ctx.author.id}').set({u'items': {"**24.** Loot Crate": crate}}, merge=True)
                    return await ctx.message.reply(f"**Your {activepet} used its ability and granted you {crate} Loot Crates!**")
                else:
                    raise error
        elif activepet == 'Polari' and lvl == 5 and xp == "MAX LEVEL":
            coins =  random.randint(100,200)
            bal = db.collection('balance').document(f"{ctx.author.id}").get().to_dict()['coins']
            db.collection('balance').document(f"{ctx.author.id}").set({'coins':bal + coins})
            return await ctx.message.reply(f"**Your {activepet} used its ability and granted you {coins}<:coin:845012771594043412>!**")
        else:
            return await ctx.message.reply(f"**Your {activepet} doesn't have an usable ability!**")

    @commands.command(aliases=['pinv','pinventory','petinv'], help="See your pet inventory.", usage="petinventory")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def petinventory(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        stuff = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        pets = []
        items = []
        ingredients = []
        dishes = []
        i=1
        for x in sorted(stuff['pets']):
            if x == 'Snom':
                pets.append(f"**{i}.** <:Snom:839487545423298571>" + x)
            elif x == 'Poochy':
                pets.append(f"**{i}.** <:Poochy:839487548488155176>" + x)
            elif x == 'Thwimp':
                pets.append(f"**{i}.** <:Thwimp:839487547574190087>" + x)
            elif x == 'Polari':
                pets.append(f"**{i}.** <:Polari:839487545686884352>" + x)
            elif x == 'Bandana Dee':
                pets.append(f"**{i}.** <:BandanaDee:839487545414910042>" + x)
            elif x == 'Baby Yoshi':
                pets.append(f"**{i}.** <:BabyYoshi:839487506583126066>" + x)
            elif x == 'Plessie':
                pets.append(f"**{i}.** <:Plessie:839487547105476638>" + x)
            elif x == 'Korok':
                pets.append(f"**{i}.** <:Korok:839487545360515127>" + x)
            elif x == 'Boo Guy':
                pets.append(f"**{i}.** <:BooGuy:839487545334038538>" + x)
            elif x == 'K. K. Slider':
                pets.append(f"**{i}.** <:K_:839487545338494986>" + x)
            elif x == 'Terrako':
                pets.append(f"**{i}.** <:Terrako:839487546144718928>" + x)
            elif x == 'Polterpup':
                pets.append(f"**{i}.** <:Polterpup:839487545321979944>" + x)
            elif x == 'Judd':
                pets.append(f"**{i}.** <:Judd:839487545473368074>" + x)
            elif x == 'Bobby':
                pets.append(f"**{i}.** <:Bobby:839487545272041492>" + x)
            else:
                pets.append(f"**{i}.** <:Mew:839487545645072406>" + x)
            i+=1
        for k,v in sorted(stuff['items'].items()):
            if k == '**1.** Pet Capsule':
                items.append(f"**1.** <:pet_capsule:838882986358997092> Pet Capsule ─ " + str(v))
            elif k == '**2.** Rare Candy':
                items.append(f"**2.** <:retard_rocky:916070708206002198> Rare Candy ─ "+ str(v))
            elif k == '**3.** Lucky Egg':
                items.append(f"**3.** <:lucky_egg:838559488683409459> Lucky Egg ─ " + str(v) + " uses left")
            elif k == 'Leash' and v == True:
                items.append(f"**4.** <:leash:839269905072652296> Leash")
            elif k == 'Shampoo' and v == True:
                items.append(f"**5.** <:wash_bucket:839272321386545182> Shampoo")
            elif k == 'Rubber Ball' and v == True:
                items.append(f"**6.** <:rubber_ball:838559474838274048> Rubber Ball")
            elif k == 'Cook Book' and v == True:
                items.append(f"**7.** <:cook_book:840326571935399946> Cook Book")
            elif k == '**8.** Sheikah Slate':
                items.append("**8.** <:sheikah_slate:842490321085923368> Sheikah Slate ─ " + str(v) + " uses left")
        i=1
        for rarities in ['Common','Rare','Very Rare', 'Legendary']:
            try:
                for k,v  in sorted(stuff['ingredients'][rarities].items()):
                    ingredients.append(f"**{i}.** {k} ─ {v}")
                    i+=1
            except Exception as error:
                pass
        i=1
        for k,v  in sorted(stuff['dishes'].items()):
            dishes.append(f"**{i}.** {k} ─ {v}")
            i+=1
        pets = '\n'.join(pets)
        if pets == None or pets == "":
            pets = "No Pets"
        items = '\n'.join(items)
        if items == None or items == "":
            items = "No Items"
        ingredients = '\n'.join(ingredients)
        if ingredients == None or ingredients == "":
            ingredients = "No Ingredients"
        dishes = '\n'.join(dishes)
        if dishes == None or dishes == "":
            dishes = "No Dishes"
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f"Use **{ctx.prefix}equip <item_name>** to equip a role and use **{ctx.prefix}use <item_name>** to use an item.")
        embed.set_author(name=f"{ctx.author.name}'s inventory", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Pets: ", value=f"{pets}")
        embed.add_field(name="Items: ", value=f"{items}", inline=False)
        embed.add_field(name="Ingredients: ", value=f"{ingredients}",inline=False)
        embed.add_field(name="Dishes: ", value=f"{dishes}",inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,25,commands.BucketType.user)
    async def hunt(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
        if bal < 25:
            return await ctx.message.reply("You don't have enough money to hunt!")
        db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal-25})
        pet = await self.getpet(ctx.author.id) 
        try:
            lasthunt = db2.collection('hunt').document(f'{ctx.author.id}').get().to_dict()['cooldown']
            then = lasthunt
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            if pet == "Poochy":
                try:
                    lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                    xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
                except Exception as error:
                    if isinstance(error,KeyError):
                        lvl = 0
                        xp = "not owned"
            if pet == 'Poochy' and lvl == 5 and xp == "MAX LEVEL":
                thendate = datetime.datetime.fromtimestamp(15+then/1e3)
            else:
                thendate = datetime.datetime.fromtimestamp(25+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can hunt again in **{str(seconds) + 's'}**")
            db2.collection(u"hunt").document(f"{ctx.author.id}").set({
                'cooldown': int(round(time.time() * 1000)),
                },merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db2.collection(u"hunt").document(f"{ctx.author.id}").set({
                'cooldown': int(round(time.time() * 1000)),
                },merge=True)
            else:
                raise error
        ingredients = {
            "Common": {
                'Goat Butter': ('<:butter:913440883372879932>', "BOTW"),
                'Fresh Milk': ('<:milk:913440883557421086>', "BOTW"),
                'Raw Gourmet Meat': ('<:ham:913440883356090379>', "BOTW"),
                'Ultra Shroom': ('<:shroom:913440883221880834>', "MARIO"),
                'Egg': ('<:paper_egg:913440883137990657>', "MARIO"),
                'Maxim Tomato': ('<:tomato:913440883658080348>', "KIRBY"),
                'Cherry': ('<:cherry:913440883347710022>', "AC")
            },
            "Rare":{
                'Cane Sugar': ('<:sugar_cane:913440883377070141>', "BOTW"),
                'Tabantha Wheat': ('<:wheat:913440883221868555>', "BOTW"),
                'Hylian Rice': ('<:wheat_but_fancier:913440883779715104>', "BOTW"),
                'Cake Mix': ('<:cake_mix:938784977598943303>', "MARIO"),
                'Carrot': ('<:carrot:913440883158970459>', "KIRBY"),
                'Bananas': ('<:banana:913440883192500295>', "KIRBY"),
                'Orange': ('<:orange:913440883586777118>', "AC")
            },
            "Very Rare":{
                'Courser Bee Honey': ('<:honey:913440883477733428>', "BOTW"),
                'Big Hearty Truffle': ('<:truffles:913440883309953055>', "BOTW"),
                'Dried Pasta': ('<:driedpasta:938789782056742963>', "MARIO"),
                'Gem Apple': ('<:shiny_apple:913440883670655036>', "KIRBY"),
                'Durian': ('<:durian:938789531895865365>', "AC"),
                'Crucian Carp': ('<:fish:913440883477717082>', "AC")
            },
            "Legendary":{
                'Fortified Pumpkin': ('<:fortifiedpumpkin:938789096623579217>', "BOTW"),
                'Big Hearty Radish': ('<:heartyradish:938788652430028831>', "BOTW"),
                'Coconut': ('<:ncoconut:938787455853789194>', "MARIO"),
                'Miracle Fruit': ('<:miraclefruit:938788297633845380>', "KIRBY"),
                'Blue Marlin': ('<:bluemarlin:938787893290348587>', "AC")
            }
        }
        try:
            sheikahs = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['**8.** Sheikah Slate']
            try:
                sheikah_category = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['sheikah']
                try:
                    rarities = ['Common', 'Rare', 'Very Rare', 'Legendary', "Nothing", "Nabbit"]
                    rarity = random.choices(rarities, weights=[40, 30, 17, 3, 5, 5], k=1)[0]
                    if rarity == "Nothing":
                        embed = discord.Embed(title=f"You arrived home from hunting but sadly you caught nothing...",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
                    elif rarity == "Nabbit":
                        try:
                            hasuno = db.collection('uno').document(f'{ctx.author.id}').get().to_dict()['activated']
                            if hasuno == "true":
                                embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost your uno card.",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                                await ctx.send(embed=embed)
                                db.collection(u'uno').document(f"{ctx.author.id}").set({u'activated': "false"}, merge=True)
                                return
                        except Exception as error:
                            if isinstance(error, TypeError):
                                pass
                            elif isinstance(error, KeyError):
                                pass
                            else:
                                raise error
                        try:
                            balance = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
                            amount_stolen = random.randint(600, 1000)
                            if balance - amount_stolen < 0:
                                balance = 0
                            else:
                                balance = balance - amount_stolen
                            embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost **{amount_stolen}**<:coin:845012771594043412>",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                            db.collection("balance").document(f"{ctx.author.id}").set({
                                "coins": balance
                            }, merge=True)
                        except Exception as error:
                            if isinstance(error, TypeError):
                                balance = 0
                            elif isinstance(error, KeyError):
                                balance = 0
                            else:
                                raise error
                        return
                    else:
                        pass
                    valid = False
                    while valid is False:
                        ingredient = random.choice(list(ingredients[rarity].keys()))
                        if ingredients[rarity][ingredient][1] == sheikah_category:
                            valid = True
                        else:
                            continue
                    if sheikahs - 1 == 0:
                        db.collection('petinventory').document(f'{ctx.author.id}').set({
                            "items": {
                                "**8.** Sheikah Slate": firestore.DELETE_FIELD
                            }
                        }, merge=True)
                    else:
                        db.collection('petinventory').document(f'{ctx.author.id}').set({
                            "items": {
                                "**8.** Sheikah Slate": sheikahs - 1
                            }
                        }, merge=True)
                except Exception as error:
                    raise error
            except Exception as error:
                if isinstance(error, KeyError):
                    rarities = ['Common','Rare','Very Rare','Legendary','Nothing','Nabbit']
                    rarity = random.choices(rarities, weights=[40,30,17,3,5,5], k=1)[0]
                    if rarity == "Nothing":
                        embed = discord.Embed(title=f"You arrived home from hunting but sadly you caught nothing...",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
                    elif rarity == "Nabbit":
                        try:
                            hasuno = db.collection('uno').document(f'{ctx.author.id}').get().to_dict()['activated']
                            if hasuno == "true":
                                embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost your uno card.",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                                await ctx.send(embed=embed)
                                db.collection(u'uno').document(f"{ctx.author.id}").set({u'activated': "false"}, merge=True)
                                return
                        except Exception as error:
                            if isinstance(error, TypeError):
                                pass
                            elif isinstance(error, KeyError):
                                pass
                            else:
                                raise error
                        try:
                            balance = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
                            amount_stolen = random.randint(300, 500)
                            if balance - amount_stolen < 0:
                                balance = 0
                            else:
                                balance = balance - amount_stolen
                            embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost **{amount_stolen}**<:coin:845012771594043412>",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                            db.collection("balance").document(f"{ctx.author.id}").set({
                                "coins": balance
                            }, merge=True)
                        except Exception as error:
                            if isinstance(error, TypeError):
                                balance = 0
                            elif isinstance(error, KeyError):
                                balance = 0
                            else:
                                raise error
                        return
                    else:
                        ingredient = random.choice(list(ingredients[rarity]))
                else:
                    raise error
        except Exception as error:
            if isinstance(error, KeyError):
                rarities = ['Common','Rare','Very Rare','Legendary','Nothing','Nabbit']
                rarity = random.choices(rarities, weights=[40,30,17,3,5,5], k=1)[0]
                if rarity == "Nothing":
                        embed = discord.Embed(title=f"You arrived home from hunting but sadly you caught nothing...",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
                elif rarity == "Nabbit":
                        try:
                            hasuno = db.collection('uno').document(f'{ctx.author.id}').get().to_dict()['activated']
                            if hasuno == "true":
                                embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost your uno card.",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                                await ctx.send(embed=embed)
                                db.collection(u'uno').document(f"{ctx.author.id}").set({u'activated': "false"}, merge=True)
                                return
                        except Exception as error:
                            if isinstance(error, TypeError):
                                pass
                            elif isinstance(error, KeyError):
                                pass
                            else:
                                raise error
                        try:
                            balance = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
                            amount_stolen = random.randint(300, 500)
                            if balance - amount_stolen < 0:
                                balance = 0
                            else:
                                balance = balance - amount_stolen
                            embed = discord.Embed(title=f"You got robbed in the forest by the Nabbit and lost **{amount_stolen}**<:coin:845012771594043412>",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                            db.collection("balance").document(f"{ctx.author.id}").set({
                                "coins": balance
                            }, merge=True)
                        except Exception as error:
                            if isinstance(error, TypeError):
                                balance = 0
                            elif isinstance(error, KeyError):
                                balance = 0
                            else:
                                raise error
                        return
                else:
                    ingredient = random.choice(list(ingredients[rarity]))
            else:
                raise error
        if pet == "Bandana Dee":
            try:
                    lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                    xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                    if isinstance(error,KeyError):
                        lvl = 0
                        xp = "not owned"
        if pet == "Bandana Dee" and lvl == 5 and xp == "MAX LEVEL":
            double = False
            chance = random.choices(["yes", "no"], weights=[20, 80], k=1)[0]
            if chance == "yes":
                _rarity = random.choices(rarities, weights=[45,35,17,3, 0, 0], k=1)[0]
                _ingredient = random.choice(list(ingredients[_rarity]))
                double = True
            if double is True:
                try:
                    ingamount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['ingredients'][rarity][ingredient]
                except Exception as error:
                    if isinstance(error,KeyError):
                        ingamount= 0
                try:
                    _ingamount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['ingredients'][_rarity][_ingredient]
                except Exception as error:
                    if isinstance(error,KeyError):
                        _ingamount= 0
                if ingredient != _ingredient:        
                    db.collection('petinventory').document(f'{ctx.author.id}').set({'ingredients':{
                        rarity:{
                            ingredient: ingamount + 1,
                        },
                    }},merge=True)
                    db.collection('petinventory').document(f'{ctx.author.id}').set({'ingredients':{
                        _rarity:{
                            _ingredient: _ingamount + 1,
                        },
                    }},merge=True)
                else:
                    db.collection('petinventory').document(f'{ctx.author.id}').set({'ingredients':{
                        rarity:{
                            ingredient: ingamount + 2,
                        },
                    }},merge=True)
                embed = discord.Embed(title=f"You arrived home from hunting!",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
                embed.add_field(name="You got:",value=f"{ingredients[rarity][ingredient][0]} {ingredient} and {ingredients[_rarity][_ingredient][0]} {_ingredient}", inline=False)
                embed.add_field(name="Rarity", value=f"{rarity}\n{_rarity}")
                embed.add_field(name="Category", value=f"{ingredients[rarity][ingredient][1]}\n{ingredients[_rarity][ingredient][1]}")
                return await ctx.send(embed=embed)
        ingamount = 0
        try:
            ingamount = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['ingredients'][rarity][ingredient]
        except Exception as error:
            if isinstance(error,KeyError):
                ingamount= 0
        db.collection('petinventory').document(f'{ctx.author.id}').set({'ingredients':{
            rarity:{
                ingredient: ingamount + 1
            }
        }},merge=True)
        embed = discord.Embed(title=f"You arrived home from hunting!",timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="You got:",value=f"{ingredients[rarity][ingredient][0]} {ingredient}")
        embed.add_field(name="Rarity", value=rarity)
        embed.add_field(name="Category", value=ingredients[rarity][ingredient][1])
        return await ctx.send(embed=embed)

    @commands.command(aliases=['pstats'])
    @commands.cooldown(1,2,commands.BucketType.user)
    async def petstats(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
        if check is None:
            return await ctx.message.reply("Please use `!setup` to setup your inventory before using any pet related command!")
        x = await self.getpet(ctx.author.id)
        if x is None or x == '':
            return await ctx.message.reply("You don't have any pet equipped!")
        embed = discord.Embed(title=f"Pet stats for {x}",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['XP']
        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][x]['Level']
        if lvl == 1:
            xpcap = 300
        elif lvl == 2:
            xpcap= 700
        elif lvl == 3:
            xpcap= 1200
        elif lvl == 4:
            xpcap= 1500
        elif lvl == 5:
            xpcap= 1900
        petname = x
        if petname == 'Bandana Dee':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165581491175474/Bandana_Dee.png'
        elif petname == 'Polari':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167546384187452/Polari.png'
        elif petname == 'Thwimp':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839167367707492362/Thwimp.png'
        elif petname == 'Poochy':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839165803793350686/Poochy.png'
        elif petname == 'Baby Yoshi':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168272083058718/Baby_Yoshi.png'
        elif petname == 'Plessie':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168498310840330/Plessie.png'
        elif petname == 'Korok':
                    peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168495957966878/Korok.png'
        elif petname == 'Boo Guy':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839168383320457216/Boo_Guy.png'
        elif petname == 'K. K. Slider':
            peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839167843714072596/K._K._Slider.png'
        elif petname == 'Snom':
            peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839165430136045618/Snom.png'
        elif petname == 'Terrako':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169275251785768/Terrako.png'
        elif petname == 'Polterpup':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169274567589908/Polterpup.png'
        elif petname == 'Judd':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/839169272437014569/Judd.png'
        elif petname == 'Bobby':
            peturl = 'https://cdn.discordapp.com/attachments/839165416508883024/845750240459489310/Bobby.png'
        else:
            peturl ='https://cdn.discordapp.com/attachments/839165416508883024/839169273464225883/Mew.png'
        embed.add_field(name="XP: ", value=f"{xp}/{xpcap}",inline=False)
        embed.add_field(name="Level: ",value=f"{lvl}",inline=False)
        embed.set_thumbnail(url=peturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pets(bot))
