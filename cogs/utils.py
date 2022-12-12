import discord
from discord.ext import commands
from firebase_admin import firestore
import typing
import datetime
import random
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import asyncio
from PIL import Image, ImageSequence
from io import BytesIO
import firebase_admin


db = firestore.client(firebase_admin._apps['maindb'])
db2 = firestore.client(firebase_admin._apps['extra-database'])

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Utils"

    async def getpet(self,user):
        try:
            pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
            return pet
        except:
            pass

    @commands.command(help="Get someone's avatar.", usage="avatar @user(optional)", aliases=["av", "pfp"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None):
        if ctx.channel.id != 728299872947667106:
            return
        if not user:
            user = ctx.author
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name=f"{user.name}'s avatar", icon_url=user.avatar_url)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Get the bot latency.", usage="ping", aliases=["latency"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        embed = discord.Embed(color=discord.Colour.gold())
        embed.add_field(
            name="Ping: ", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.command(aliases=["reportbug", "bugrep", "bug"], help="Report bugs and problems with the bot.", usage="bugreport <bug> (description of the problem encountered - detailed if possible)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bugreport(self, ctx, *, bug):
        if ctx.channel.id != 728299872947667106:
            return
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), title="Bug Report")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.description = f"Oh no... What's wrong with me...? :disappointed_relieved:\n\nThank you, {ctx.author.mention}, for reporting this issue. It has been submitted and my devs will take a look (or more) into it."
        await ctx.send(embed=embed)
        bug_report_channel = await self.bot.fetch_channel(835200680251097089)
        bug_embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), title="Bug Report")
        bug_embed.add_field(name="Submitted by", value=f"**User: **{ctx.author.mention}\n**Name: **{ctx.author}\n**ID: **{ctx.author.id}\n**In: **{ctx.channel.name}")
        bug_embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        bug_embed.description = bug
        await bug_report_channel.send(embed=bug_embed)

    @commands.command(help="Shows your inventory.", usage="inventory", aliases=["inv"])
    @commands.cooldown(1,2, commands.BucketType.user)
    async def inventory(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        itemss = db.collection(u"inventory").document(f"{ctx.author.id}").get().to_dict()
        _items = db.collection(u"items").document(f"{ctx.author.id}").get()
        roles = []
        collectibles = []
        items = []
        if itemss['items'] == []:
            roles = "No roles"
        else:
            for value in sorted(itemss["items"]):
                if value >= 1 or value <= 15:
                    if str(value) == '1':
                        roles.append('**1.**White')
                    if str(value) == '2':
                        roles.append('**2.**Brown')
                    if str(value) == '3':
                        roles.append('**3.**Orange')
                    if str(value) == '4':
                        roles.append('**4.**Yellow')
                    if str(value) == '5':
                        roles.append('**5.**Pink')
                    if str(value) == '6':
                        roles.append('**6.**Dark Blue')
                    if str(value) == '7':
                        roles.append('**7.**Dark Green')
                    if str(value) == '8':
                        roles.append('**8.**Red')
                    if str(value) == '9':
                        roles.append('**9.**Light Green')
                    if str(value) == '10':
                        roles.append('**10.**Black')
                    if str(value) == '11':
                        roles.append('**11.**Sky Blue')
                    if str(value) == '12':
                        roles.append('**12.**Gold')
                    if str(value) == '13':
                        roles.append('**13.**Aquamarine')
                    if str(value) == '14':
                        roles.append('**14.**Purple')
                    if str(value) == '15':
                        roles.append('**15.**Maroon')
        if _items is None:
            items = "No items"
        else:
            for key,value in sorted(_items.to_dict()['items'].items()):
                if key == "**23.** Mystery Egg":
                    items.append("**23.** <a:yoshi_egg:751188866840395856> Mystery Egg ─ " + str(value))
                elif key == "**24.** Loot Crate":
                    items.append("**24.** <a:loot_box:913440884018774036> Loot Crate ─ " + str(value))
                elif key == "**25.** Uno Reverse Card":
                    items.append("**25.** <:uno_reverse_card:913440883653877840> Uno Reverse Card ─ " + str(value))
                elif key == "**26.** Fish Bait":
                    items.append(f"**26.** <:bait:842452124469297182> Fish Bait ─ {value} uses left")
                elif key == "**27.** Nabbit":
                    items.append("**27.** <a:nabbit:735156984420106320> Nabbit ─ " + str(value))
                elif key == "**28.** Nickname Badge":
                    items.append("**28.** :scroll: Nickname Badge")
                elif key == "**29.** DJ Badge":
                    items.append("**29.** :dvd: DJ Badge")
        collectibles = '\n'.join(collectibles)
        items = '\n'.join(items)
        if roles == None or roles == "" or roles == "No roles":
            roles = "No roles"
        else:
            roles = '\n'.join(roles)
        if items == None or items == "":
            items = "No items"
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f"Use **{ctx.prefix}equip <item_name>** to equip a role and use **{ctx.prefix}use <item_name>** to use an item.")
        embed.set_author(name=f"{ctx.author.name}'s inventory", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Roles: ", value=f"{roles}")
        embed.add_field(name="Items: ", value=f"{items}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Equip a role in your inventory.", usage="equip <role_name>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def equip(self, ctx, *, args: typing.Optional[str]):
        # if ctx.channel.id != 728299872947667106:
        #     return
        if not args:
            embed = discord.Embed(title="Invalid use of `equip`!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error:", value="```Role not found```")
            return await ctx.message.reply(embed=embed)
        roles = {
            "white": (1, "White"), "1": (1, "White"),

            "brown": (2, "Brown"), "2": (2, "Brown"),

            "orange": (3, "Orange"), "3": (3, "Orange"),

            "yellow": (4, "Yellow"), "4": (4, "Yellow"),

            "pink": (5, "Pink"), "5": (5, "Pink"),

            "dark blue": (6, "Dark Blue"), "dblue": (5000, 6, "Dark Blue"), "darkblue": (6, "Dark Blue"), "6": (6, "Dark Blue"),

            "dark green": (7, "Dark Green"), "dgreen": (5000, 7, "Dark Green"), "darkgreen": (7, "Dark Green"), "7": (7, "Dark Green"),

            "red": (8, "Red"), "8": (8, "Red"),

            "light green": (9, "Light Green"), "lgreen": (5000, 9, "Light Green"), "lightgreen": (9, "Light Green"), "9": (9, "Light Green"),

            "black": (10, "Black"), "10": (10, "Black"),

            "sky blue": (11, "Sky Blue"), "sblue": (11, "Sky Blue"), "skyblue": (11, "Sky Blue"), "11": (11, "Sky Blue"),

            "gold": (12, "Gold"), "12": (12, "Gold"),

            "aqua marine": (13, "Aquamarine"), "aquamarine": (13, "Aquamarine"), "13": (13, "Aquamarine"),

            "purple": (14, "Purple"), "14": (14, "Purple"),

            "maroon": (15, "Maroon"), "15": (15, "Maroon"),

            "nickname badge": ('**28.** Nickname Badge', "〈 📜 〉"), "nickname": ('**28.** Nickname Badge', "〈 📜 〉"), "nick": ('**28.** Nickname Badge', "〈 📜 〉"), "28": ('**28.** Nickname Badge', "〈 📜 〉"),

            "dj badge": ('**29.** DJ Badge',"〈 📀 〉"), "dj": ('**29.** DJ Badge', "〈 📀 〉"), "29": ('**29.** DJ Badge', "〈 📀 〉")
        }
        items = db.collection(u'inventory').document(f'{ctx.author.id}').get().to_dict()['items']
        usables = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']
        if roles[args.lower()][0] in items or roles[args.lower()][0] in usables:
            role = discord.utils.get(ctx.guild.roles,name=f"{roles[args.lower()][1]}")
            if role is None:
                perms = discord.Permissions(send_messages=False, read_messages=True)
                await ctx.guild.create_role(name=f"{roles[args.lower()][1]}", permissions=perms)
                role = discord.utils.get(ctx.guild.roles, name=f"{roles[args.lower()][1]}")
            await ctx.author.add_roles(role)
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            if role == "〈 📀 〉":
                embed.description = "```DJ Role added!```"
            elif role == "〈 📜 〉":
                embed.description = "```Nickname Role added!```"
            else:
                embed.description = f"```{role} added!```"
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error:", value="```You don't own that role```")
            return await ctx.message.reply(embed=embed)

    @commands.command(help="Unequip a role in your inventory.", usage="unequip <role_name>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unequip(self, ctx, *, args: typing.Optional[str]):
        # if ctx.channel.id != 728299872947667106:
        #     return
        if not args:
            embed = discord.Embed(title="Invalid use of `equip`!",color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error:", value="```Role not found```")
            return await ctx.message.reply(embed=embed)
        x = args[0].upper()
        lenarg = -len(args)
        roles = []
        role = None
        for y in ctx.author.roles:
            roles.append(y.name.lower())
        if args == "nickname" or args == "nickname badge":
            if "〈 📜 〉" in roles:
                role = discord.utils.find(lambda r: r.name == '〈 📜 〉', ctx.author.roles)
        elif args == "dj" or args == "dj badge":
             if "〈 📀 〉" in roles:
                role = discord.utils.find(lambda r: r.name == '〈 📀 〉', ctx.author.roles)
        else:
            role = discord.utils.find(lambda r: r.name.lower() == f'{(x + args[lenarg+1:]).lower()}', ctx.author.roles)
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        if role is None or role == "None":
            embed.color = discord.Color.red()
            embed.add_field(name="Error", value=f"```You don't have {args} equipped```")
        elif role == "〈 📀 〉":
            await ctx.author.remove_roles(role)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.description = "```DJ Role unequipped!```"
        elif role == "〈 📜 〉":
            await ctx.author.remove_roles(role)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.description = "```Nickname Badge unequipped!```"
        else:
            await ctx.author.remove_roles(role)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.description = f"```{role} unequipped!```"
        await ctx.send(embed=embed)

    @staticmethod
    def yoshi_gif(buffer: BytesIO, resize: tuple):
        buffer.seek(0)
        avatar = Image.open(buffer)
        avatar = avatar.resize(resize)
        avatar = avatar.convert("RGBA")

        background = Image.new('RGBA', (300, 169), (255, 255, 255, 0))
        gif = Image.open("./images/yoshi-short-crop.gif")

        frames = []
        for img in ImageSequence.Iterator(gif):
            frame_bg = background.copy().convert('RGBA')
            frame_gif = img.copy().convert('RGBA')
            frame_bg.paste(frame_gif, (0, 0), frame_gif)
            frame_bg.paste(avatar, (203, 50), avatar)
            frames.append(frame_bg.convert('RGBA'))

        final_buffer = BytesIO()
        frames[0].save(final_buffer, format='gif', save_all=True, append_images=frames[1:], loop=0, duration=45, optimize=True)
        final_buffer.seek(0)
        return final_buffer

    @commands.group(help="Uses an item from your inventory.", usage="use <item>", case_insensitive=True)
    @commands.cooldown(1,2,commands.BucketType.user)
    async def use(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"**Please specify an item.**\n*ex: {ctx.prefix}use <item>*", color=discord.Color.gold())
            embed.add_field(name="Available Items:", value="*Mystery Egg, Loot Crate, Uno Reverse Card, Nabbit*")
            await ctx.send(embed=embed)

    @use.command(aliases=["mystery", "mystery egg", "23"], help="Gift someone a Mystery Egg.", usage="use mystery egg")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def mysteryegg(self, ctx, user: typing.Optional[discord.Member]):
        if ctx.channel.id != 728299872947667106:
            return
        crates = random.randint(1, 5)
        try:
            authoritems = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()
            if not "**23.** Mystery Egg" in authoritems['items']:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {}})
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        if user is None:
            embed = discord.Embed(title="You need to mention someone!", description="Be kind and gift this to someone", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            return await ctx.message.reply(embed=embed)
        elif user.id is ctx.author.id:
            embed = discord.Embed(title="Invalid use of `mystery egg`!", description="You can't gift it to yourself!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            return await ctx.message.reply(embed=embed)
        try:
            inv = db.collection("items").document(f"{user.id}").get().to_dict()
            db.collection("items").document(f"{user.id}").set({u'items':
            {
                "**24.** Loot Crate": inv["items"]["**24.** Loot Crate"] + crates
            }}, merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{user.id}').set({u'items': {"**24.** Loot Crate": crates}}, merge=True)
            elif isinstance(error,KeyError):
                db.collection(u'items').document(f'{user.id}').set({u'items': {"**24.** Loot Crate": crates}}, merge=True)
            else:
                raise error
        mysteryammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']['**23.** Mystery Egg']
        db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {'**23.** Mystery Egg': mysteryammount-1}}, merge=True)
        mysteryammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']['**23.** Mystery Egg']
        if mysteryammount == 0:
            db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {'**23.** Mystery Egg': firestore.DELETE_FIELD}}, merge=True)
        embed=discord.Embed(
            title=f"{ctx.author.name} gifted {crates} Loot Crates to {user.name} using the Mystery Egg!",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/832685967898705960/843899610832830534/yoshi_egg.gif")
        embed.set_footer(text=f"Good Luck {user.name}!",icon_url=ctx.guild.icon_url)
        return await ctx.send(embed=embed)

    @use.command(aliases=["loot crate", "loot", "crate", "24"], help="Use a loot box to get random loot.", usage="use lootcrate")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lootcrate(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        coins = random.randint(150, 250)
        item = random.randint(1, 7)
        try:
            authoritems = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()
            if not "**24.** Loot Crate" in authoritems['items']:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {}})
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        if item == 1:
            try:
                unocards = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**25.** Uno Reverse Card']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**25.** Uno Reverse Card": unocards + 1}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**25.** Uno Reverse Card": 1}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.add_field(name="Loot: ",value="Uno Reverse Card <:uno_reverse:734938966528360580> **x1**.")
        if item == 2:
            try:
                yoshieggs = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**26.** Fish Bait']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**26.** Fish Bait": yoshieggs + 15}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**26.** Fish Bait": 15}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.add_field(name="Loot: ",value="Fish Bait <:bait:842452124469297182> **x15**.")
        if item == 3:
            try:
                nabbitamount = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**27.** Nabbit']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**27.** Nabbit": nabbitamount + 1}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**27.** Nabbit": 1}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.add_field(name="Loot: ",value="Nabbit <a:nabbit:735156984420106320> **x1**.")
        if item >= 4 and item <=7:
            try:
                bal = db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins']
                db.collection('balance').document(f'{ctx.author.id}').set({'coins': bal + coins},merge=True)
            except Exception as error:
                if isinstance(error, TypeError):
                    db.collection('balance').document(f'{ctx.author.id}').set({'coins': coins},merge=True)
                else:
                    raise error
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.add_field(name="Coins: ",value=f"{coins}<:coin:845012771594043412>")
        await ctx.send(embed=embed)
        lootamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']['**24.** Loot Crate']
        db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**24.** Loot Crate': lootamount-1}}, merge=True)
        lootamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**24.** Loot Crate']
        if lootamount == 0:
            db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**24.** Loot Crate': firestore.DELETE_FIELD}}, merge=True)
    
    @use.command(aliases=["uno", "uno reverse", "uno reverse card", "uno card", "reverse card", "reverse", "card", "25"], help="Activate your uno card to block people from stealing from you.", usage="use unoreversecard")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def unoreversecard(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        try:
            authoritems = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()
            if not "**25.** Uno Reverse Card" in authoritems['items']:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {}})
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        try:
            unoactivated = db.collection(u'uno').document(f'{ctx.author.id}').get().to_dict()["activated"]
            if unoactivated == "false":
                db.collection(u'uno').document(f'{ctx.author.id}').set({'activated': "true"},merge=True)
                embed = discord.Embed(title="UNO Reverse Card activated!", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                unoamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']['**25.** Uno Reverse Card']
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**25.** Uno Reverse Card': unoamount-1}}, merge=True)
                unoamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**25.** Uno Reverse Card']
                if unoamount == 0:
                    db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**25.** Uno Reverse Card': firestore.DELETE_FIELD}}, merge=True)
                return await ctx.send(embed=embed)
            if unoactivated == "true":
                embed = discord.Embed(title="UNO Reverse Card already activated!", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'uno').document(f'{ctx.author.id}').set({'activated': "true"},merge=True)
                embed = discord.Embed(title="UNO Reverse Card activated!", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                unoamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items']['**25.** Uno Reverse Card']
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**25.** Uno Reverse Card': unoamount-1}}, merge=True)
                unoamount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**25.** Uno Reverse Card']
                if unoamount == 0:
                    db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**25.** Uno Reverse Card': firestore.DELETE_FIELD}}, merge=True)
                return await ctx.send(embed=embed)
            else:
                raise error

    @use.command(help="Steal money from someone.", usage="use nabbit", aliases=["27"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def nabbit(self,ctx,user:typing.Optional[discord.Member]):
        if ctx.channel.id != 728299872947667106:
            return
        try:
            mode = db.collection(u'nabbit').document(f"{ctx.author.id}").get().to_dict()['mode']
            if mode == "aggressive":
                pass
            elif mode == "passive":
                embed = discord.Embed(description="You are in passive mode. You can't rob or be robbed.", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                db.collection(u'nabbit').document(f"{ctx.author.id}").set({"mode": "aggressive"}, merge=True)
            else:
                raise error
        try:
            mode = db.collection(u'nabbit').document(f"{user.id}").get().to_dict()['mode']
            if mode == "aggressive":
                pass
            elif mode == "passive":
                embed = discord.Embed(description="User is in passive mode and can't get robbed", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                db.collection(u'nabbit').document(f"{ctx.author.id}").set({"mode": "aggressive"}, merge=True)
            else:
                raise error
        try:
            authoritems = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()
            if not "**27.** Nabbit" in authoritems['items']:
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{ctx.author.id}').set({'items': {}})
                embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return await ctx.message.reply(embed=embed)
            else:
                raise error
        if not user:
            embed = discord.Embed(title="Invalid use of `use` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
            embed.add_field(name="Error:",value="User Not Found!")
            return await ctx.message.reply(embed=embed)
        if user.id == ctx.author.id:
            return await ctx.message.reply("You can't rob yourself.")
        if db.collection(u'balance').document(f"{user.id}").get().to_dict()['coins'] < 500:
                embed = discord.Embed(title=f"{user.name} has less than 500 coins and can't get robbed!",
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Colour.random())
                return await ctx.message.reply(embed=embed)
        try:
            pet = await self.getpet(ctx.author.id)
            lastnabbit = db.collection('nabbit').document(f'{ctx.author.id}').get().to_dict()['cooldown']
            then = lastnabbit
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
            if pet == "K. K. Slider" and lvl == 5 and xp == "MAX LEVEL":
                thendate = datetime.datetime.fromtimestamp(300+then/1e3)
            else:
                thendate = datetime.datetime.fromtimestamp(600+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can rob someone again in **{str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"nabbit").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"nabbit").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
            elif isinstance(error,KeyError):
                db.collection(u"nabbit").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
            else:
                raise error
        try:
            lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
            xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
        except Exception as error:
            if isinstance(error,KeyError):
                lvl = 0
                xp = "not owned"
        if pet == 'Boo Guy' and lvl == 5 and xp == "MAX LEVEL":
            coins = random.randint(400,500)
        else:
            coins = random.randint(300,500)
        if pet =='Thwimp' and lvl == 5 and xp == "MAX LEVEL":
            fail = random.randint(1,10)
        else:
            fail = random.randint(1,5)
        responses = ["Nope. - <a:nabbit:735156984420106320>", "You tried to use your Nabbit but he was asleep and you couldn't manage to wake him up."]
        if fail == 1:
            nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
            db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': nabbitammount-1}}, merge=True)
            nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
            if nabbitammount == 0:
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': firestore.DELETE_FIELD}}, merge=True)
            return await ctx.message.reply(random.choice(responses))
        try:
            hasuno = db.collection('uno').document(f'{user.id}').get().to_dict()['activated']
            if hasuno == "true":
                if db.collection(u'balance').document(f"{ctx.author.id}").get().to_dict()['coins'] <= 250:
                    db.collection(u'balance').document(f"{ctx.author.id}").set({u'coins': 0}, merge=True)
                else:
                    db.collection(u'balance').document(f"{ctx.author.id}").set({u'coins': db.collection(u'balance').document(f"{ctx.author.id}").get().to_dict()['coins'] - 250}, merge=True)
                db.collection(u'balance').document(f"{user.id}").set({u'coins': db.collection(u'balance').document(f"{user.id}").get().to_dict()['coins'] + 250}, merge=True)
                db.collection(u'uno').document(f"{user.id}").set({u'activated': "false"}, merge=True)
                embed = discord.Embed(title=f"{user.name} used UNO Reverse Card!",
                                    timestamp=datetime.datetime.utcnow(), 
                                    color=discord.Colour.gold())
                embed.add_field(name="Reversed your steal and you lost: ", value=f"250 <:coin:845012771594043412>!")
                await ctx.message.reply(embed=embed)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': nabbitammount-1}}, merge=True)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                if nabbitammount == 0:
                    db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': firestore.DELETE_FIELD}}, merge=True)
            else:
                db.collection(u'balance').document(f"{ctx.author.id}").set({u'coins': db.collection(u'balance').document(f"{ctx.author.id}").get().to_dict()['coins'] + coins}, merge=True)
                db.collection(u'balance').document(f"{user.id}").set({u'coins': db.collection(u'balance').document(f"{user.id}").get().to_dict()['coins'] - coins}, merge=True)
                embed = discord.Embed(title=f"{ctx.author.name} just robbed {user.name} for {coins}!",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
                await ctx.send(embed=embed)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': nabbitammount-1}}, merge=True)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                if nabbitammount == 0:
                    db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': firestore.DELETE_FIELD}}, merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection('uno').document(f'{user.id}').set({'activated': "false"},merge=True)
                hasuno = db.collection('uno').document(f'{user.id}').get().to_dict()['activated']
                db.collection(u'balance').document(f"{ctx.author.id}").set({u'coins': db.collection(u'balance').document(f"{ctx.author.id}").get().to_dict()['coins'] + coins}, merge=True)
                db.collection(u'balance').document(f"{user.id}").set({u'coins': db.collection(u'balance').document(f"{user.id}").get().to_dict()['coins'] - coins}, merge=True)
                embed = discord.Embed(title=f"{ctx.author.name} just robbed {user.name} for {coins}!",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
                await ctx.send(embed=embed)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': nabbitammount-1}}, merge=True)
                nabbitammount = db.collection(u'items').document(f"{ctx.author.id}").get().to_dict()['items'][f'**27.** Nabbit']
                if nabbitammount == 0:
                    db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {f'**27.** Nabbit': firestore.DELETE_FIELD}}, merge=True)
            else:
                raise error

    @commands.command(help="Switch between passive (you can't rob or be robbed) and aggressive (you can rob and be robbed) modes on nabbit.", usage="nabbitmode <mode>", aliases=["nmode"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def passive(self, ctx, mode: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        if mode is None:
            return await ctx.message.reply("***No mode specified. Choose between `enabled` and `disabled`.***")
        mode = mode.lower()
        if mode != "enabled" and mode != "disabled":
            return await ctx.message.reply("***Not a valid mode!***")
        try:
            activemode = db.collection(u'nabbit').document(f"{ctx.author.id}").get().to_dict()['mode']
        except Exception as error:
            if isinstance(error,KeyError):
                db.collection(u'nabbit').document(f"{ctx.author.id}").set({'mode': "aggressive"})
                activemode = "aggressive"
        if activemode == "aggressive" and mode == "disabled":
            return await ctx.message.reply(f"***Mode already set to {mode}!***")
        elif activemode == "passive" and mode == "enabled":
            return await ctx.message.reply(f"***Mode already set to {mode}!***")
        try:
            lastmode = db.collection('nabbit').document(f'{ctx.author.id}').get().to_dict()['modecd']
            then = lastmode
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can set your nabbit mode again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"nabbit").document(f"{ctx.author.id}").set({u'modecd': int(round(time.time() * 1000))},merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection('nabbit').document(f'{ctx.author.id}').set({'modecd':int(round(time.time()*1000))}, merge=True)
            elif isinstance(error, KeyError):
                db.collection('nabbit').document(f'{ctx.author.id}').set({'modecd':int(round(time.time()*1000))}, merge=True)
            else:
                raise error
        if mode == "enabled":
            db.collection(u"nabbit").document(f"{ctx.author.id}").set({"mode": "passive"},merge=True)
        elif mode == "disabled":
            db.collection(u"nabbit").document(f"{ctx.author.id}").set({"mode": "aggressive"},merge=True)
        embed = discord.Embed(description=f"Successfully changed nabbit mode.", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @staticmethod
    def get_cooldown(user_id: int, collection: str, cooldown_str: str, seconds: int, function_index: int):
        try:
            if collection == "coinflip":
                last = db2.collection(collection).document(f"{user_id}").get()
            else:
                last = db.collection(collection).document(f"{user_id}").get()
            then = last.to_dict()[cooldown_str]
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(seconds+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            days = timeleft.days
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return [str(days) + 'd ' + str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's', function_index]
        except Exception as error:
            if isinstance(error,TypeError):
                return ["No Cooldown", function_index]
        return ["No Cooldown", function_index]

    @commands.command(help="See your cooldowns.", usage="cooldowns", aliases=["cooldowns", "cooldown"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cd(self, ctx):
        # if ctx.channel.id != 728299872947667106:
        #     return
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
        embed.set_author(name=f"{ctx.author.name}'s cooldowns", icon_url=ctx.author.avatar_url)

        param_list = [("daily", "dailycooldown", 86400), ("weekly", "weeklycooldown", 604800),
                      ("coinflip", "cooldown", 600), ("nabbit", "cooldown", 600), ("premium", "cooldown", 86400)]

        with ThreadPoolExecutor() as thread_pool:
            futures = []
            x = 0
            for param1, param2, param3 in param_list:
                futures.append(thread_pool.submit(self.get_cooldown, user_id=ctx.author.id, collection=param1, cooldown_str=param2, seconds=param3, function_index=x))
                x += 1
            result_list = []
            for future in concurrent.futures.as_completed(futures):
                result_list.append(future.result())

        for result in result_list:
            if result[1] == 0:
                daily = result[0]
            elif result[1] == 1:
                weekly = result[0]
            elif result[1] == 2:
                coinflip = result[0]
            elif result[1] == 3:
                nabbit = result[0]
            elif result[1] == 4:
                premium = result[0]

        premium_role = discord.utils.get(ctx.guild.roles, id=727634503962591345)
        if premium_role in ctx.author.roles:
            embed.add_field(name="**Premium Cooldown**", value=f"```fix\n{premium}\n```", inline=False)
        else:
            pass
        embed.add_field(name="**Daily Reward Cooldown**", value=f"```fix\n{daily}\n```", inline=False)
        embed.add_field(name="**Weekly Reward Cooldown**", value=f"```fix\n{weekly}\n```", inline=False)
        embed.add_field(name="**Coinflip Cooldown**", value=f"```fix\n{coinflip}\n```", inline=False)
        embed.add_field(name="**Nabbit Cooldown**", value=f"```fix\n{nabbit}\n```", inline=False)

        await ctx.send(embed=embed)
    
    @commands.command(help="Bumps this server <3.", usage="d bump", aliases=["d bump"])
    async def d(self,ctx, *, args:typing.Optional[str]):
        if ctx.channel.id != 732787014444777494:
            return
        if args.lower() != "bump" or args is None:
            return
        _time = db.collection("bump").document("cooldown").get().to_dict()['time']
        today = int(round(time.time() * 1000))
        todaydate = datetime.datetime.fromtimestamp(today/1e3)
        thendate = datetime.datetime.fromtimestamp(7200+_time/1e3)
        timeleft = abs(todaydate-thendate)
        seconds = timeleft.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if todaydate < thendate:
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.description = f"You can bump again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**"
            return await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, thanks for bumping NSK! \n <:arrow:752022451600228452> You have been awarded 100<:rupee:752022419363069952>!")
            db.collection("bump").document("cooldown").set({'time': int(round(time.time() * 1000))})
            db.collection("balance").document(f"{ctx.author.id}").set({'coins': db.collection("balance").document(f"{ctx.author.id}").get().to_dict()['coins'] + 100})

    @commands.command(help="If you've found yourself in the situation of wanting to get the cover art of a Spotify track, this command can help you out (it literally does nothing more).",
        usage="spotify @user (optional)"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def spotify(self, ctx, member: discord.Member=None):
        if ctx.channel.id != 728299872947667106:
            return
        if not member:
            member = ctx.message.author
        embed = discord.Embed(timestamp=datetime.datetime.utcnow())
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        if not member.activity:
            embed.color = 0xde2f43
            embed.description = ':x: No activity detected.'
            return await ctx.send(embed=embed)
        else:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    embed.color = 0x1DB954
                    embed.title = activity.title
                    embed.url = f"https://open.spotify.com/track/{activity.track_id}"
                    embed.set_author(name='Spotify', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/753667014827966464/spotify.png')
                    embed.description = ', '.join(activity.artists)
                    embed.description = f'**by**: {embed.description}\n**on**: {activity.album}'
                    embed.set_image(url=activity.album_cover_url)
                    embed.set_thumbnail(url=member.avatar_url)
            if not embed.description:
                embed.color = 0xde2f43
                embed.description = ':x: No Spotify activity detected.'
        return await ctx.send(embed=embed)

    @commands.command(aliases=['uinfo', 'about', 'whois'], help="Get info about yourself or someone else.",
        usage="userinfo @user (optional)"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member=None):
        if ctx.channel.id != 728299872947667106:
            return
        if not member:
            member = ctx.message.author
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=member.mention)
        if member.public_flags.hypesquad_balance:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659063759667280/balance.png')
        elif member.public_flags.hypesquad_bravery:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659066246365184/bravery.png')
        elif member.public_flags.hypesquad_brilliance:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659069224189962/brilliance.png')
        else:
            embed.set_author(name=f'{member}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        if member.status is discord.Status.online:
            embed.add_field(name='**Status**', value=f'```css\n+{member.status}\n```', inline=True)
        elif member.status is discord.Status.dnd:
            embed.add_field(name='**Status**', value=f'```diff\n-{member.status}\n```', inline=True)
        elif member.status is discord.Status.idle:
            embed.add_field(name='**Status**', value=f'```fix\n{member.status}\n```', inline=True)
        elif member.status is discord.Status.offline:
            embed.add_field(name='**Status**', value=f'```css\n.{member.status}\n```', inline=True)
        if member.activity == None:
            activity = 'None'
        else:
            activity = member.activity.name
        reg = member.created_at.__format__('%a, %d %b %Y %H:%M')
        join = member.joined_at.__format__('%a, %d %b %Y %H:%M')
        embed.add_field(name='**Activity**', value=f'```bash\n"{activity}"\n```', inline=True)
        embed.add_field(name='**Nickname**', value=f'```css\n[{member.nick}]\n```', inline=True)
        embed.add_field(name='**ID**', value=f'```diff\n-{member.id}\n```', inline=True)
        then = member.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        days = str(age).split(',', 1)
        embed.add_field(name='**Registered**', value=f'```ini\n[{reg} ({days[0]})]\n```', inline=True)
        then = member.joined_at
        age = now - then
        days = str(age).split(',', 1)
        embed.add_field(name='**Joined**', value=f'```ini\n[{join} ({days[0]})]\n```', inline=False)
        allroles = list(map(lambda x: x.mention, member.roles[::-1]))
        allroles = allroles[:-1]
        allroles = ' '.join(allroles)
        if allroles:
            embed.add_field(name=f'**Roles** ({len(member.roles)-1})', value=allroles, inline=False)
        else:
            embed.add_field(name='**Roles** (0)', value='```css\n[None]\n```', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'aboutsrv'], help="Get info about the server.", usage="serverinfo")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=ctx.guild.icon_url, name=f'{ctx.guild} Server Info')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        embed.add_field(name='**Owner**', value=f'```fix\n{ctx.guild.owner}\n```')
        embed.add_field(name='**Region**', value=f'```ini\n[{ctx.guild.region}]\n```', inline=True)
        created = ctx.guild.created_at.__format__('%A, %d %B %Y %H:%M')
        then = ctx.guild.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        age = str(age)
        days = list(age.split(',', 1))
        embed.add_field(name='**Created**', value=f'```ini\n[{created} ({days[0]})]\n```', inline=True)
        embed.add_field(name='**ID**', value=f'```diff\n-{ctx.guild.id} (guild)  -{ctx.guild.owner.id} (owner)\n```', inline=False)
        embed.add_field(name='**Text Channels**', value=f'```fix\n{len(ctx.guild.text_channels)}\n```', inline=True)
        embed.add_field(name='**Voice Channels**', value=f'```fix\n{len(ctx.guild.voice_channels)}\n```', inline=True)
        embed.add_field(name='**Emotes**', value=f'```fix\n{len(ctx.guild.emojis)}\n```')
        bots = sum(member.bot for member in ctx.guild.members)
        online = sum(member.status == discord.Status.online and not member.bot for member in ctx.guild.members)
        dnd = sum(member.status == discord.Status.dnd and not member.bot for member in ctx.guild.members)
        idle = sum(member.status == discord.Status.idle and not member.bot for member in ctx.guild.members)
        off = sum(member.status == discord.Status.offline and not member.bot for member in ctx.guild.members)
        embed.add_field(name='**Members**', value=f'```diff\n-{ctx.guild.member_count} ({bots} bots)\n-on: {online} | dnd: {dnd} | idle: {idle} | off: {off}\n```')
        allroles = list(map(lambda x: x.mention, ctx.guild.roles[::-1]))
        allroles = allroles[:-1]
        allroles = ' '.join(allroles)
        embed.add_field(name=f'**Roles** ({len(ctx.guild.roles)-1})', value=allroles, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['rinfo'], help="Get info about a role.", usage="roleinfo @role")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roleinfo(self, ctx, role : discord.Role):
        if ctx.channel.id != 728299872947667106:
            return
        embed = discord.Embed(description=role.mention, color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f'Role Info {role}', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='**ID**', value=f'```diff\n-{role.id}\n```')
        created = role.created_at.__format__('%A, %d %B %Y %H:%M')
        embed.add_field(name='**Color**', value=f'```fix\n{role.color}\n```')
        embed.add_field(name='**Mentionable**', value=f'```diff\n-{role.mentionable}\n```')
        then = role.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        age = str(age)
        days = list(age.split(',', 1))
        embed.add_field(name='**Created**', value=f'```ini\n[{created} ({days[0]})]\n```')
        embed.add_field(name='**Members**', value=f'```fix\n{len(role.members)}\n```')
        if role.hoist is False:
            embed.add_field(name='**Hoisted**', value=f'```css\n[{role.hoist}]\n```')
        else:
            embed.add_field(name='**Hoisted**', value=f'```ini\n[{role.hoist}]\n```')
        await ctx.send(embed=embed)

    @commands.command(aliases=['perms', 'userperms'], help="See a user's guild permissions.",
        usage="permissions @user (optional)"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def permissions(self, ctx, member : discord.Member=None):
        if ctx.channel.id != 728299872947667106:
            return
        if not member:
            member = ctx.message.author
        perms = ', '.join(perm.capitalize() for perm, value in member.guild_permissions if value)
        perms = perms.replace('_', ' ')
        embed = discord.Embed(description=f'{member.mention}\n```ini\n[{perms}]\n```', color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=member.avatar_url, name=f'Guild Permissions {member}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['rperms', 'roleperms'], help="See the permissions of a role.")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rpermissions(self, ctx, *, role : discord.Role):
        if ctx.channel.id != 728299872947667106:
            return
        perms = ', '.join(perm.capitalize() for perm, value in role.permissions if value)
        perms = perms.replace('_', ' ')
        embed = discord.Embed(description=f'{role.mention}\n```css\n[{perms}]\n```', color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=ctx.guild.icon_url, name=f"Role Permissions {role}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['startup'],help="Teaches you the basics of the bot!")
    @commands.cooldown(1,2,commands.BucketType.user)
    async def start(self,ctx):
        if ctx.channel.id != 728299872947667106:
            return
        msg = await ctx.message.reply("Command started in DMS.")
        message = await ctx.author.send("Start by doing !daily and !weekly in #bot-commands and then come back and say \"Done\".")
        await asyncio.sleep(0.25)
        await msg.delete()
        def check(m):
            return (m.content == 'done' or m.content == 'Done')  and m.author == ctx.author
        msg = await self.bot.wait_for('message', check=check)
        if msg.content.lower() == "done":
            await message.delete()
            message = await ctx.author.send("Good now try fishing by doing !fish in #bot-commands and then come back and say \"Done\".")
            def check(m):
                return (m.content == 'done' or m.content == "Done" ) and m.author == ctx.author
            msg = await self.bot.wait_for('message', check=check)
            if msg.content.lower() == "done":
                await message.delete()
                message = await ctx.author.send("Well done! Now take a look into the shop by doing !shop items/roles/pets in #bot-commands and then come back and say \"Done\".")
                def check(m):
                    return (m.content == 'done' or m.content == "Done" ) and m.author == ctx.author
                msg = await self.bot.wait_for('message', check=check)
                if msg.content.lower() == "done":
                    await message.delete()
                    message = await ctx.author.send("Now for the last step! Type !inventory in #bot-commands. There will be all your collected items. To use any usable item from there (when you will have any) you just have to do `!use item_number` or `!use item_name`! \nThat's all! To end the tutorial say \"done\"")
                    def check(m):
                        return (m.content == 'done' or m.content == "Done" ) and m.author == ctx.author
                    msg = await self.bot.wait_for('message', check=check)
                    if msg.content.lower() == "done":
                        await message.delete()
                        await ctx.author.send("For a more in-depth view do !help! There you can view the categories on commands and then you can do `!help \"command_name\"`")

def setup(bot):
    bot.add_cog(Utils(bot))
