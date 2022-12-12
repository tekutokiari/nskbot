import discord
from discord.ext import commands
from discord.ext.commands import errors
from firebase_admin import firestore
import datetime
from dpymenus import Page, PaginatedMenu
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import typing
import time
import random
import firebase_admin

db = firestore.client(firebase_admin._apps['maindb'])
db2 = firestore.client(firebase_admin._apps['extra-database'])

def is_owner(ctx):
    return ctx.author.id in [465138950223167499, 449555448010375201,450883984600072193,396002772568506369]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Economy"

    async def getpet(self,user):
        try:
            pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
            return pet
        except:
            pass

    def _getpet(self,user):
        try:
            pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
            return pet
        except:
            pass

    @commands.command(help="Claim your daily loot crate as a premium NSK member.", usage="premium")
    async def premium(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        role = discord.utils.get(ctx.guild.roles, id=727634503962591345)
        if role not in ctx.author.roles:
            embed = discord.Embed(description="You are not a premium NSK member :(", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        try:
            lastpremium = db.collection('premium').document(f'{ctx.author.id}').get().to_dict()['cooldown']
            then = lastpremium
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can claim your premium rewards again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"premium").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection('premium').document(f'{ctx.author.id}').set({'cooldown':int(round(time.time()*1000))}, merge=True)
            elif isinstance(error, KeyError):
                db.collection('premium').document(f'{ctx.author.id}').set({'cooldown':int(round(time.time()*1000))}, merge=True)
            else:
                raise error
        coins = random.randint(200, 500)
        item = random.randint(1, 7)
        if item == 1:
            try:
                unocards = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**25.** Uno Reverse Card']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**25.** Uno Reverse Card": unocards + 1}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**25.** Uno Reverse Card": 1}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Loot: ",value="Uno Reverse Card <:uno_reverse_card:913440883653877840> **x1**.")
        if item == 2:
            try:
                bait = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**26.** Fish Bait']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**26.** Fish Bait": bait + 15}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**26.** Fish Bait": 15}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Loot: ",value="Fish Bait <:bait:842452124469297182> **x15**.")
        if item == 3:
            try:
                nabbitamount = db.collection('items').document(f'{ctx.author.id}').get().to_dict()['items']['**27.** Nabbit']
                db.collection('items').document(f'{ctx.author.id}').set({'items': {"**27.** Nabbit": nabbitamount + 1}},merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection('items').document(f'{ctx.author.id}').set({'items': {"**27.** Nabbit": 1}},merge=True)
            embed = discord.Embed(title="You unboxed a loot crate and got",timestamp=datetime.datetime.utcnow(), color=discord.Colour.gold())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Coins: ",value=f"{coins}<:coin:845012771594043412>")
        await ctx.send(embed=embed)

    @commands.command(help="Check a NSK credit balance.", usage="balance @user (optional)", aliases=["bal"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        if ctx.channel.id != 728299872947667106:
            return
        if user is None:
            user = ctx.author
        balance = db.collection("balance").document(f"{user.id}").get()
        shinybalance = db.collection("shiny").document(f"{user.id}").get()
        if balance.exists and shinybalance.exists:
            embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
            embed.add_field(name="Coins", value=f"{balance.to_dict()['coins']} <:coin:845012771594043412>")
            embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
            await ctx.send(embed=embed)
        elif not balance.exists or not shinybalance.exists:
            createbalance = db.collection("balance").document(f"{user.id}")
            createbalance.set({
                'coins': 0
            }, merge=True)
            createshiny = db.collection("shiny").document(f"{user.id}")
            createshiny.set({
                'shiny': 0
            }, merge=True)
            db.collection(u'inventory').document(f"{user.id}").set({u'items': []},merge=True)
            db.collection(u'items').document(f"{user.id}").set({u'items': {}},merge=True)
            balance = db.collection("balance").document(f"{user.id}").get()
            shinybalance = db.collection("shiny").document(f"{user.id}").get()
            embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
            embed.add_field(name="Coins", value=f"{balance.to_dict()['coins']} <:coin:845012771594043412>")
            embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
            await ctx.send(embed=embed)

    @commands.command(help="Add an amount of NSK coins to someone.", usage="addcoins <amount> @user")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.check(is_owner)
    async def addcoins(self, ctx, user: typing.Optional[discord.Member], amount:typing.Optional[int]):
        if ctx.channel.id != 728299872947667106:
            return
        if user is None:
            user = ctx.author
        if amount is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount not found!```")
            return await ctx.message.reply(embed=embed)
        balance = db.collection("balance").document(f"{user.id}").get().to_dict()["coins"]
        if amount < 1:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be lower than 1!```")
            return await ctx.message.reply(embed=embed)
        db.collection("balance").document(f"{user.id}").update({ "coins": balance + amount})
        shinybalance = db.collection("shiny").document(f"{user.id}").get()
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
        embed.add_field(name="Coins", value=f"{balance + amount} <:coin:845012771594043412>")
        embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
        await ctx.send(embed=embed)

    @commands.command(help="Remove an amount of NSK coins from someone.", usage="removecoins <amount> @user")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.check(is_owner)
    async def removecoins(self, ctx, user: typing.Optional[discord.Member], amount:typing.Optional[int]):
        if ctx.channel.id != 728299872947667106:
            return
        if user is None:
            user = ctx.author
        if amount is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount not found!```")
            return await ctx.message.reply(embed=embed)
        balance = db.collection("balance").document(f"{user.id}").get().to_dict()["coins"]
        if amount > balance:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be greater than user's amount of coins!```")
            return await ctx.message.reply(embed=embed)
        db.collection("balance").document(f"{user.id}").update({ "coins": balance - amount})
        shinybalance = db.collection("shiny").document(f"{user.id}").get()
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
        embed.add_field(name="Coins", value=f"{balance - amount} <:coin:845012771594043412>")
        embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
        await ctx.send(embed=embed)

    @commands.command(help="Add an amount of NSK shiny coins to someone.", usage="addshiny <amount> @user")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.check(is_owner)
    async def addshiny(self, ctx, amount: int, user: discord.Member = None):
        if ctx.channel.id != 728299872947667106:
            return
        if user is None:
            user = ctx.author
        balance = db.collection("shiny").document(f"{user.id}").get().to_dict()["shiny"]
        if amount < 1:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be lower than 1!```")
            return await ctx.message.reply(embed=embed)
        db.collection("shiny").document(f"{user.id}").update({ "shiny": balance + amount})
        coins = db.collection("balance").document(f"{user.id}").get()
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
        embed.add_field(name="Coins", value=f"{coins.to_dict()['coins']} <:coin:845012771594043412>")
        embed.add_field(name="Shiny rupees", value=f"{balance + amount} <:1_shiny_rupee:755974674927845456>")
        await ctx.send(embed=embed)

    @commands.command(help="Remove an amount of NSK shiny coins from someone.", usage="removeshiny <amount> @user")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.check(is_owner)
    async def removeshiny(self, ctx, user: typing.Optional[discord.Member], amount:typing.Optional[int]):
        if ctx.channel.id != 728299872947667106:
            return
        if user is None:
            user = ctx.author
        if amount is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount not found!```")
            return await ctx.message.reply(embed=embed)
        balance = db.collection("shiny").document(f"{user.id}").get().to_dict()["shiny"]
        if amount > balance:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be greater than user's amount of shiny rupees!```")
            return await ctx.send(embed=embed)
        db.collection("shiny").document(f"{user.id}").update({ "shiny": balance - amount})
        coins = db.collection("balance").document(f"{user.id}").get()
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar_url)
        embed.add_field(name="Coins", value=f"{coins.to_dict()['coins']} <:coin:845012771594043412>")
        embed.add_field(name="Shiny rupees", value=f"{balance - amount} <:1_shiny_rupee:755974674927845456>")
        await ctx.send(embed=embed)

    @commands.command(help="Transfer an amount of NSK coins to someone.", usage="transfer @user <amount>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def transfer(self, ctx, user: typing.Optional[discord.Member],amount: typing.Optional[int]):
        if ctx.channel.id != 728299872947667106:
            return
        if not user:
            embed = discord.Embed(title="Incorect use of `transfer` command!", timestamp=datetime.datetime.utcnow(),color=discord.Colour.red())
            embed.add_field(name="Error:", value="```Missing User!```")
            return await ctx.message.reply(embed=embed)
        elif user.id == ctx.author.id:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```You can't give yourself money!```")
            return await ctx.message.reply(embed=embed)
        elif not user and not amount:
            embed = discord.Embed(title="Incorect use of `transfer` command!", timestamp=datetime.datetime.utcnow(),color=discord.Colour.red())
            embed.add_field(name="Correct use", value=f"```{ctx.prefix}transfer @user <amount>```")
            return await ctx.message.reply(embed=embed)
        elif user and not amount:
            embed = discord.Embed(title="Incorect use of `transfer` command!", timestamp=datetime.datetime.utcnow(),color=discord.Colour.red())
            embed.add_field(name="Error:", value="```Missing Amount!```")
            return await ctx.message.reply(embed=embed)
        authorbalance = db.collection("balance").document(f"{ctx.author.id}").get()
        userbalance = db.collection("balance").document(f"{user.id}").get()
        authorbal = authorbalance.to_dict()["coins"]
        userbal = userbalance.to_dict()["coins"]
        _authorbal = authorbal
        _userbal = userbal
        if amount > authorbal:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```You can't give out more money than you have!```")
            await ctx.message.reply(embed=embed)
        elif amount < 1:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```You can't give an amount lower than 1!```")
            await ctx.message.reply(embed=embed)
        else:
            _userbal = _userbal + amount
            _authorbal = _authorbal - amount
            authorbalance = db.collection("balance").document(f"{ctx.author.id}").update({
                'coins': _authorbal
            })
            userbalance = db.collection("balance").document(f"{user.id}").set({
                'coins': _userbal
            })
            embed = discord.Embed(description=f"{ctx.author.mention} transfered ***{amount}***<:coin:845012771594043412> to {user.mention}", color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)

    @commands.command(help="Convert 50.000 coins into 1 Shiny Rupee.", usage="buyrupee")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def buyrupee(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        shiny = db.collection("shiny").document(f"{ctx.author.id}").get().to_dict()["shiny"]
        coins = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
        if coins < 50000:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```You don't have enough coins!```")
            return await ctx.message.reply(embed=embed)
        db.collection("shiny").document(f"{ctx.author.id}").set({
            "shiny": shiny + 1
        }, merge=True)
        db.collection("balance").document(f"{ctx.author.id}").set({
            "coins": coins - 50000
        }, merge=True)
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{ctx.author.name}'s balance", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Coins", value=f"{coins - 50000} <:coin:845012771594043412>")
        embed.add_field(name="Shiny rupees", value=f"{shiny + 1} <:1_shiny_rupee:755974674927845456>")
        await ctx.send(embed=embed)

    @staticmethod
    async def create_pages(items: list, prices: list, title: str, description: str, menu: PaginatedMenu):
        items_per_page = 0
        page_list = []
        color = discord.Color.gold()
        page = Page(title=title, description=description, color=color, timestamp=datetime.datetime.utcnow())
        for i in range(0, len(items)):
            page.add_field(name=items[i], value=prices[i], inline=False)
            items_per_page += 1
            if  items_per_page == 5:
                items_per_page = 0
                page_list.append(page)
                page = Page(title=title, description=description, color=color, timestamp=datetime.datetime.utcnow())
        if items_per_page > 0:
            page_list.append(page)
        menu.add_pages(page_list)

    @staticmethod
    async def create_bg_pages(img_urls: list, menu: PaginatedMenu, prefix: str):
        i = 1
        page_list = []
        for url in img_urls:
            page = Page(title="Profile Backgrounds Shop", description=f"Use {prefix}buybg `{i}` to buy this background\n\n **Price: **1000 <:coin:845012771594043412>", color=discord.Color.gold())
            page.set_image(url=url)
            page_list.append(page)
            i += 1
        menu.add_pages(page_list)

    @commands.group(help="Shows the items currently available in the market.", usage="shop <category>", aliases=["market"], case_insensitive=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def shop(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"Please specify a category.\n*ex: {ctx.prefix}shop <category>*", color=discord.Color.gold())
            embed.set_author(icon_url=self.bot.user.avatar_url, name="NS Kingdom Shop")
            embed.add_field(name="Available Categories", value=f"*roles, items, backgrounds (`{ctx.prefix}buybg`), pets(`{ctx.prefix}petshop`)*")
            await ctx.send(embed=embed)

    @shop.command(help="Role shop.", usage="shop roles")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roles(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        items = [
            "1. White", "2. Brown", "3. Orange", "4. Yellow", "5. Pink", "6. Dark Blue", "7. Dark Green", "8. Red", "9. Light Green", "10. Black",
            "11. Sky Blue", "12. Gold", "13. Aquamarine", "14. Purple", "15. Maroon"
        ]
        prices = [
            "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>",
            "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>",
            "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>", "Price: 5000 <:coin:845012771594043412>"
        ]
        title, description = "Roles Shop", f"Use {ctx.prefix}buy `name` to buy a role"
        menu = PaginatedMenu(ctx)
        menu.show_skip_buttons()
        await self.create_pages(items, prices, title, description, menu)
        await menu.open()

    @shop.command(help="Item shop.", usage="shop items")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def items(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        items = [
            "23. Mystery Egg <a:yoshi_egg:751188866840395856>", "24. Loot crate <a:loot_box:913440884018774036>", "25. Uno Reverse Card <:uno_reverse_card:913440883653877840>",
            "26. Fish Bait <:bait:842452124469297182>", "27. Nabbit <a:nabbit:735156984420106320>", "28. Nickname Badge :scroll:", "29. DJ Badge :dvd:"
        ]
        prices = [
            "️️<:arrow:752022451600228452> Gives mentioned user between 1-5 Loot Crates! <a:loot_box:913440884018774036> \nPrice: 1000 <:coin:845012771594043412>",
            "<:arrow:752022451600228452> Unbox 200-500 <:coin:845012771594043412> or a random item.\nPrice: Only obtained from !daily and !weekly",
            "<:arrow:752022451600228452> Deflect and rob the nabbit user.\nPrice: 350 <:coin:845012771594043412>",
            "<:arrow:752022451600228452> Pack of 15 fish bait. Increases chances for Eep Cheeps but also for unlucky reels.\nPrice: 200 <:coin:845012771594043412>",
            "<:arrow:752022451600228452> Steals 300-500 <:coin:845012771594043412> from a selected user.\nPrice: 250 <:coin:845012771594043412>",
            "<:arrow:752022451600228452> Gives the permission to change your nickname.\nPrice: 15000 <:coin:845012771594043412>",
            "<:arrow:752022451600228452> Gives DJ permission.\nPrice: 15000 <:coin:845012771594043412>"
        ]
        title, description = "Items Shop", f"Use {ctx.prefix}buy `name` to buy an item"
        menu = PaginatedMenu(ctx)
        menu.show_skip_buttons()
        await self.create_pages(items, prices, title, description, menu)
        await menu.open()

    @shop.command(help="Profile backgrounds shop.", usage="shop backgrounds", aliases=["bg", "profile bg", "profile backgrounds"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def backgrounds(self, ctx):
        if ctx.channel.id != 728299872947667106:
           return
        images = [
            "https://cdn.discordapp.com/attachments/838417288452374568/838417389620166676/1.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417404387524628/2.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417421592690728/3.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417428635582464/4.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417434481393674/5.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417442908274718/6.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417454504869908/7.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417463959355442/8.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417472784826378/9.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417479600308224/10.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417480312553472/11.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417489331355678/12.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417497677234229/13.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417507105636362/14.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417519685009418/15.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417525892841472/16.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417536479133716/17.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417547266883664/18.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417559832363069/19.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417581257261136/20.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417588996407316/21.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417598658904074/22.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417609614426162/23.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417621593620520/24.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417631329255464/25.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417640603123752/26.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417651759841331/27.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417665310588929/28.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417674320216114/29.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417686044082186/30.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417695804227604/31.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417703873806386/32.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417723067203614/33.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417732285497384/34.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417753588629504/35.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417766129336330/36.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417774115553300/37.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417782613213184/38.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417793208680528/39.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417802682564688/40.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417823382110268/41.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417840079896634/42.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417847016489070/43.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417856358121504/44.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417867045077012/45.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417878122102804/46.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417889631535155/47.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417899487363092/48.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417913475760178/49.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417922338193428/50.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417935160574022/51.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417947655274526/52.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417955645292614/53.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417963622727720/54.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417970958565396/55.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417978960773151/56.jpg"
        ]
        menu = PaginatedMenu(ctx)
        menu.show_skip_buttons()
        menu.set_timeout(120)
        await self.create_bg_pages(images, menu, ctx.prefix)
        await menu.open()

    @staticmethod
    def buy_one_time_item(buyer: discord.Member, price: int, array_union_index: int, you_got: str):
        try:
            bal = db.collection("balance").document(f"{buyer.id}").get().to_dict()['coins']
        except Exception as error:
            if isinstance(error, TypeError):
                createbalance = db.collection("balance").document(f"{buyer.id}")
                createbalance.set({
                    'coins': 0
                }, merge=True)
                createshiny = db.collection("shiny").document(f"{buyer.id}")
                createshiny.set({
                    'shiny': 0
                }, merge=True)
                bal = db.collection("balance").document(f"{buyer.id}").get().to_dict()['coins']
            else:
                raise error
        try:
            inventory = db.collection("inventory").document(f"{buyer.id}").get().to_dict()['items']
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection(u'items').document(f'{buyer.id}').set({u'items': {}}, merge=True)  # pt iteme uzabile
                db.collection(u'inventory').document(f'{buyer.id}').set({u'items': {}}, merge=True)  # pt role-uri si collectible non uzabile
                inventory = db.collection("inventory").document(f"{buyer.id}").get().to_dict()['items']
            else:
                raise error
        for x in sorted(inventory):
            if x == array_union_index:
                return "***You already own this.***"
        if bal < price:
            return "***You don't have enough money.***"
        else:
            db.collection("balance").document(f"{buyer.id}").update({"coins": bal - price})
            items = db.collection("inventory").document(f"{buyer.id}")
            items.update({
                u'items':
                    firestore.ArrayUnion([array_union_index])
                    })
            embed = discord.Embed(title="Transaction successful!", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=buyer.name, icon_url=buyer.avatar_url)
            embed.add_field(name="You paid:", value=f"**{price}** <:coin:845012771594043412>")
            embed.add_field(name="You got:", value=you_got)
            return embed

    @staticmethod
    def buy_usable_item(buyer: discord.Member, price: int, inventory_key: str, you_got: str, amount_added: int):
        try:
            bal = db.collection("balance").document(f"{buyer.id}").get().to_dict()['coins']
        except Exception as error:
            if isinstance(error, TypeError):
                createbalance = db.collection("balance").document(f"{buyer.id}")
                createbalance.set({
                    'coins': 0
                }, merge=True)
                createshiny = db.collection("shiny").document(f"{buyer.id}")
                createshiny.set({
                    'shiny': 0
                }, merge=True)
                bal = db.collection("balance").document(f"{buyer.id}").get().to_dict()['coins']
            else:
                raise error
        if bal < price:
                return "***You don't have enough money.***"
        else:
            db.collection("balance").document(f"{buyer.id}").update({"coins" : bal - price})
            items = db.collection(u"items").document(f"{buyer.id}").get()
            ok = 0
            for key, value in items.to_dict()['items'].items():
                if key == inventory_key:
                    ok = 1
                    lootnr = value
                    db.collection(u"items").document(f"{buyer.id}").set({
                        'items':{
                            inventory_key: lootnr + amount_added
                        }
                    },merge=True)
            if ok == 0:
                db.collection(u"items").document(f"{buyer.id}").set({
                    'items':{
                        inventory_key: amount_added
                    }
                }, merge=True)
            embed = discord.Embed(title="Transaction successful!",color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=buyer.name, icon_url=buyer.avatar_url)
            embed.add_field(name="You paid:", value=f"**{price}** <:coin:845012771594043412>")
            embed.add_field(name="You got:", value=you_got)
            return embed

    @staticmethod
    def buy_background(buyer: discord.Member, price:int,background_index: int, background_url: str):
        try:
            bal = db.collection("balance").document(f"{buyer.id}").get().to_dict()['coins']
        except Exception as error:
            if isinstance(error, TypeError):
                createbalance = db.collection("balance").document(f"{buyer.id}")
                createbalance.set({
                    'coins': 0
                }, merge=True)
                createshiny = db.collection("shiny").document(f"{buyer.id}")
                createshiny.set({
                    'shiny': 0
                }, merge=True)
                return "***You don't have enough money.***"
            else:
                raise error
        if bal < price:
            return "***You don't have enough money.***"
        db.collection("balance").document(f"{buyer.id}").set({
            "coins": bal - price
        }, merge=True)
        try:
            owned_bgs = db.collection("profile").document(f"{buyer.id}").get().to_dict()["ownedbgs"]
            if background_index in owned_bgs:
                return "***You already own this background.***"
            owned_bgs.append(background_index)
            db.collection("profile").document(f"{buyer.id}").set({
                "ownedbgs": owned_bgs,
                "bgset": background_index
            }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection("profile").document(f"{buyer.id}").set({
                    "ownedbgs": [0, background_index],
                    "bgset": background_index
                }, merge=True)
            else:
                raise error
        embed = discord.Embed(title="Transaction successful!",color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=buyer.name, icon_url=buyer.avatar_url)
        embed.add_field(name="You paid:", value=f"**{price}** <:coin:845012771594043412>")
        embed.add_field(name="You got:", value=f"**Background: ** `{background_index}`")
        embed.set_image(url=background_url)
        return embed

    @commands.command(help="Buy items from the shop.", usage="buy <item>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def buy(self, ctx, *, item: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        if item is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```No item specified!```")
            return await ctx.message.reply(embed=embed)
        item = item.lower()
        thread_pool = ThreadPoolExecutor(max_workers=1)
        shop_unusable_dict = {
            "white": (5000, 1, "**Color:** White"), "1": (5000, 1, "**Color:** White"),

            "brown": (5000, 2, "**Color:** Brown"), "2": (5000, 2, "**Color:** Brown"),

            "orange": (5000, 3, "**Color:** Orange"), "3": (5000, 3, "**Color:** Orange"),

            "yellow": (5000, 4, "**Color:** Yellow"), "4": (5000, 4, "**Color:** Yellow"),

            "pink": (5000, 5, "**Color:** Pink"), "5": (5000, 5, "**Color:** Pink"),

            "dark blue": (5000, 6, "**Color:** Dark Blue"), "dblue": (5000, 6, "**Color:** Dark Blue"), "darkblue": (5000, 6, "**Color:** Dark Blue"), "6": (5000, 6, "**Color:** Dark Blue"),

            "dark green": (5000, 7, "**Color:** Dark Green"), "dgreen": (5000, 7, "**Color:** Dark Green"), "darkgreen": (5000, 7, "**Color:** Dark Green"), "7": (5000, 7, "**Color:** Dark Green"),

            "red": (5000, 8, "**Color:** Red"), "8": (5000, 8, "**Color:** Red"),

            "light green": (5000, 9, "**Color:** Light Green"), "lgreen": (5000, 9, "**Color:** Light Green"), "lightgreen": (5000, 9, "**Color:** Light Green"), "9": (5000, 9, "**Color:** Light Green"),

            "black": (5000, 10, "**Color:** Black"), "10": (5000, 10, "**Color:** Black"),

            "sky blue": (5000, 11, "**Color:** Sky Blue"), "sblue": (5000, 11, "**Color:** Sky Blue"), "skyblue": (5000, 11, "**Color:** Sky Blue"), "11": (5000, 11, "**Color:** Sky Blue"),

            "gold": (5000, 12, "**Color:** Gold"), "12": (5000, 12, "**Color:** Gold"),

            "aqua marine": (5000, 13, "**Color:** Aquamarine"), "aquamarine": (5000, 13, "**Color:** Aquamarine"), "13": (5000, 13, "**Color:** Aquamarine"),

            "purple": (5000, 14, "**Color:** Purple"), "14": (5000, 14, "**Color:** Purple"),

            "maroon": (5000, 15, "**Color:** Maroon"), "15": (5000, 15, "**Color:** Maroon"),
        }
        shop_usable_dict = {
            "mystery egg": (1000, "**23.** Mystery Egg", "**Item:** Mystery Egg <a:yoshi_egg:751188866840395856>", 1), 
            "mystery": (1000, "**23.** Mystery Egg", "**Item:** Mystery Egg <a:yoshi_egg:751188866840395856>", 1), 
            "23": (1000, "**23.** Mystery Egg", "**Item:** Mystery Egg <a:yoshi_egg:751188866840395856>", 1),

            "uno reverse card": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1), "uno card": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1),
            "reverse card": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1), "uno reverse": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1),
            "uno": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1), "reverse": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1),
            "card": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1), "25": (350, "**25.** Uno Reverse Card", "**Item:** Uno Reverse Card <:uno_reverse_card:913440883653877840>", 1),
            
            "bait": (200, "**26.** Fish Bait", "**Item:** Fish Bait <:bait:842452124469297182>", 15), "fish bait": (200, "**26.** Fish Bait", "**Item:** Fish Bait <:bait:842452124469297182>", 15),

            "nabbit": (250, "**27.** Nabbit", "**Item:** Nabbit <a:nabbit:735156984420106320>", 1), "27": (250, "**27.** Nabbit", "**Item:** Nabbit <a:nabbit:735156984420106320>", 1),

            "nickname badge": (15000, "**28.** Nickname Badge", "**Item:** Nickname Badge :scroll:", 1), "nickname": (15000, "**28.** Nickname Badge", "**Item:** Nickname Badge :scroll:", 1),
            "nick": (15000, "**28.** Nickname Badge", "**Item:** Nickname Badge :scroll:", 1), "28": (15000, "**28.** Nickname Badge", "**Item:** Nickname Badge :scroll:", 1),

            "dj badge": (15000, "**29.** DJ Badge", "**Item:** DJ Badge :dvd:", 1), "dj": (15000, "**29.** DJ Badge", "**Item:** DJ Badge :dvd:", 1), "29": (15000, "**29.** DJ Badge", "**Item:** DJ Badge :dvd:", 1),

        }
        try:
            item_from_shop = shop_unusable_dict[item]
            pet = await self.getpet(ctx.author.id)
            try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
            if pet == "Terrako" and lvl == 5 and xp == "MAX LEVEL":
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
                        partial_buy_item = partial(self.buy_one_time_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2])
                    else:
                        message = await ctx.message.reply(f"```You want to use the daily discount from pet ability on {item_from_shop[2]}? If not press the ❌ to cancel the command else press the ✅!```")
                        await message.add_reaction('✅')
                        await message.add_reaction('❌')
                        reaction,user = await self.bot.wait_for('reaction_add', check = lambda reaction,user: user == ctx.author and (reaction.emoji == '✅' or reaction.emoji == '❌'))
                        if reaction.emoji == '✅':
                            y = int(item_from_shop[0] - (item_from_shop[0]* 15 /100))
                            await message.delete()
                            partial_buy_item = partial(self.buy_one_time_item, ctx.author, y, item_from_shop[1], item_from_shop[2])
                            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                                'ability': int(round(time.time() * 1000)),
                            }},merge=True)
                        else:
                            await message.delete()
                            partial_buy_item = partial(self.buy_one_time_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2])
                except Exception as error:
                    if isinstance(error,TypeError):
                        db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                            'ability':int(round(time.time() * 1000)),
                        }},merge=True)
                    else:
                        raise error
            else:
                partial_buy_item = partial(self.buy_one_time_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2])
        except Exception as error:
            if isinstance(error, KeyError):
                try:
                    item_from_shop = shop_usable_dict[item]
                    pet = await self.getpet(ctx.author.id)
                    try:
                        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
                    except Exception as error:
                        if isinstance(error,KeyError):
                            lvl = 0
                            xp = "not owned"
                    if pet == "Terrako" and lvl == 5 and xp == "MAX LEVEL":
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
                                partial_buy_item = partial(self.buy_usable_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2], item_from_shop[3])
                            else:
                                if item_from_shop[1] != '**28.** Nickname Badge' or item_from_shop[1] != '**29.** DJ Badge':
                                    message = await ctx.message.reply(f"```You want to use the daily discount from pet ability on {item_from_shop[1]}? If not press the ❌ to cancel the command else press the ✅!```")
                                    await message.add_reaction('✅')
                                    await message.add_reaction('❌')
                                    reaction,user = await self.bot.wait_for('reaction_add', check = lambda reaction,user: user == ctx.author and (reaction.emoji == '✅' or reaction.emoji == '❌'))
                                    if reaction.emoji == '✅':
                                        await message.delete()
                                        y = int(item_from_shop[0] - (item_from_shop[0]* 15 /100))
                                        partial_buy_item = partial(self.buy_usable_item, ctx.author, y, item_from_shop[1], item_from_shop[2], item_from_shop[3])
                                        db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                                            'ability':int(round(time.time() * 1000)),
                                        }},merge=True)
                                    else:
                                        await message.delete()
                                        partial_buy_item = partial(self.buy_usable_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2], item_from_shop[3])
                        except Exception as error:
                            if isinstance(error,TypeError):
                                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                                    'ability':int(round(time.time() * 1000)),
                                }},merge=True)
                            else:
                                raise error
                    else:
                        partial_buy_item = partial(self.buy_usable_item, ctx.author, item_from_shop[0], item_from_shop[1], item_from_shop[2], item_from_shop[3])
                except Exception as error:
                    if isinstance(error, KeyError):
                        return await ctx.message.reply("***That's not an item you can buy.***")
                    else:
                        raise error
            else:
                raise error
        result = await self.bot.loop.run_in_executor(thread_pool, partial_buy_item)
        if type(result) is discord.Embed:
            await ctx.send(embed=result)
        else:
            await ctx.message.reply(result)

    @commands.command(help="Buy profile backgrounds.", usage="buybg `number`", aliases=["buybackground", "bgbuy", "backgroundbuy"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def buybg(self, ctx, index: int):
        if ctx.channel.id != 728299872947667106:
            return
        if index not in range(1, 57):
            return await ctx.message.reply("***Background inexistent.***")
        images = [
            "https://cdn.discordapp.com/attachments/838417288452374568/838417389620166676/1.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417404387524628/2.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417421592690728/3.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417428635582464/4.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417434481393674/5.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417442908274718/6.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417454504869908/7.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417463959355442/8.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417472784826378/9.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417479600308224/10.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417480312553472/11.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417489331355678/12.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417497677234229/13.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417507105636362/14.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417519685009418/15.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417525892841472/16.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417536479133716/17.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417547266883664/18.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417559832363069/19.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417581257261136/20.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417588996407316/21.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417598658904074/22.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417609614426162/23.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417621593620520/24.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417631329255464/25.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417640603123752/26.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417651759841331/27.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417665310588929/28.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417674320216114/29.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417686044082186/30.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417695804227604/31.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417703873806386/32.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417723067203614/33.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417732285497384/34.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417753588629504/35.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417766129336330/36.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417774115553300/37.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417782613213184/38.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417793208680528/39.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417802682564688/40.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417823382110268/41.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417840079896634/42.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417847016489070/43.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417856358121504/44.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417867045077012/45.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417878122102804/46.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417889631535155/47.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417899487363092/48.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417913475760178/49.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417922338193428/50.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417935160574022/51.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417947655274526/52.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417955645292614/53.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417963622727720/54.jpg",
            "https://cdn.discordapp.com/attachments/838417288452374568/838417970958565396/55.jpg", "https://cdn.discordapp.com/attachments/838417288452374568/838417978960773151/56.jpg"
        ]
        thread_pool = ThreadPoolExecutor()
        pet = await self.getpet(ctx.author.id)
        try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
        except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
        if pet == "Terrako" and lvl == 5 and xp == "MAX LEVEL":
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
                    partial_buy_bg = partial(self.buy_background, ctx.author, 1000, index, images[index-1])
                else:
                    message = await ctx.message.reply(f"```You want to use the daily discount from pet ability on this background? If not press the ❌ to cancel the command else press the ✅!```")
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    reaction,user = await self.bot.wait_for('reaction_add', check = lambda reaction,user: user == ctx.author and (reaction.emoji == '✅' or reaction.emoji == '❌'))
                    if reaction.emoji == '✅':
                        await message.delete()
                        y = int(1000 - (1000* 15 /100))
                        partial_buy_bg = partial(self.buy_background, ctx.author, y, index, images[index-1])
                        db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                        'ability': int(round(time.time() * 1000)),
                        }},merge=True)
                    else:
                        await message.delete()
                        partial_buy_bg = partial(self.buy_background, ctx.author, 1000, index, images[index-1])
            except Exception as error:
                if isinstance(error,TypeError):
                    db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                        'ability':int(round(time.time() * 1000)),
                    }},merge=True)
                else:
                    raise error
        else:
            partial_buy_bg = partial(self.buy_background, ctx.author, 1000, index, images[index-1])
        result = await self.bot.loop.run_in_executor(thread_pool, partial_buy_bg)
        if type(result) is discord.Embed:
            await ctx.send(embed=result)
        else:
            await ctx.message.reply(result)

    @staticmethod
    def sell_usable_item(seller: discord.Member, item_db_key: str, name: str, price: int):
        try:
            authoritems = db.collection(u'items').document(f'{seller.id}').get().to_dict()
            if not item_db_key in authoritems['items']:
                embed = discord.Embed(title="Invalid use of `sell` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return embed
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u'items').document(f'{seller.id}').set({'items': {}})
                embed = discord.Embed(title="Invalid use of `sell` command!",timestamp=datetime.datetime.utcnow(),color=discord.Color.gold())
                embed.add_field(name="Error:",value="Item not owned!")
                return embed
            else:
                raise error
        amount = db.collection(u'items').document(f"{seller.id}").get().to_dict()['items'][item_db_key]
        db.collection(u'items').document(f"{seller.id}").set({u'items': {item_db_key: amount-1}}, merge=True)
        amount = db.collection(u'items').document(f"{seller.id}").get().to_dict()['items'][item_db_key]
        if amount == 0:
            db.collection(u'items').document(f"{seller.id}").set({u'items': {item_db_key: firestore.DELETE_FIELD}}, merge=True)
        balance = db.collection("balance").document(f"{seller.id}").get().to_dict()["coins"]
        db.collection("balance").document(f"{seller.id}").update({ "coins": balance + price})
        embed = discord.Embed(title="Transaction successful!",color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=seller.name, icon_url=seller.avatar_url)
        embed.add_field(name="You sold:", value=name)
        embed.add_field(name="Price:", value=f"**{price}** <:coin:845012771594043412>")
        return embed

    @commands.group(help="Sell items from your inventory for 75% their shop value.", usage="sell <item>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def sell(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        if ctx.invoked_subcommand is None:
            await ctx.message.reply("***Specify an item to sell!***")
    
    @sell.command(help="Sell a mystery egg.", usage="sell mysterybox", aliases=["mystery", "box", "mystery egg", "23"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def mysterybox(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        thread_pool = ThreadPoolExecutor()
        partial_mystery = partial(self.sell_usable_item, ctx.author, "**23.** Mystery Egg", "Mystery Egg", 750)
        result = await self.bot.loop.run_in_executor(thread_pool, partial_mystery)
        return await ctx.send(embed=result)

    @sell.command(help="Sell a reverse card.", usage="sell unoreversecard", aliases=["uno", "uno reverse", "uno reverse card", "uno card", "reverse card", "reverse", "card", "25"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unoreversecard(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        thread_pool = ThreadPoolExecutor()
        partial_mystery = partial(self.sell_usable_item, ctx.author, "**25.** Uno Reverse Card", "Uno Reverse Card", 263)
        result = await self.bot.loop.run_in_executor(thread_pool, partial_mystery)
        return await ctx.send(embed=result)

    @sell.command(help="Sell a nabbit.", usage="sell nabbit", aliases=["27"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def nabbit(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        thread_pool = ThreadPoolExecutor()
        partial_mystery = partial(self.sell_usable_item, ctx.author, "**27.** Nabbit", "Nabbit", 188)
        result = await self.bot.loop.run_in_executor(thread_pool, partial_mystery)
        return await ctx.send(embed=result)
    @commands.command(help="Get your daily reward. Cooldown resets 24h after the last daily.", usage="daily")
    async def daily(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        balance = db.collection("balance").document(f"{ctx.author.id}").get()
        shinybalance = db.collection("shiny").document(f"{ctx.author.id}").get()
        if not balance.exists or not shinybalance.exists:
            createbalance = db.collection("balance").document(f"{ctx.author.id}")
            createbalance.set({
                'coins': 0
            }, merge=True)
            createshiny = db.collection("shiny").document(f"{ctx.author.id}")
            createshiny.set({
                'shiny': 0
            }, merge=True)
            db.collection(u'inventory').document(f"{ctx.author.id}").set({u'items': []},merge=True)
            db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {}},merge=True)
        lastdaily = db.collection(u"daily").document(f"{ctx.author.id}").get()
        laststreak =  db.collection(u"streak").document(f"{ctx.author.id}").get()
        boxchance = random.randint(0,1)
        item = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()['items'].items()
        crate = '**24.** Loot Crate'
        amount = 50
        try:
            nrstreak = db.collection(u"streak").document(f"{ctx.author.id}").get().to_dict()['streak']
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"streak").document(f"{ctx.author.id}").set({'streak':1})
        pet = await self.getpet(ctx.author.id)
        if pet == 'Plessie':
            try:
                    lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                    xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                    if isinstance(error,KeyError):
                        lvl = 0
                        xp = "not owned"
        if pet == 'Plessie' and lvl == 5 and xp == "MAX LEVEL":
            if nrstreak >= 10 and nrstreak <=49:
                amount += 25
            elif nrstreak >=50 and nrstreak<=99:
                amount += 100
            elif nrstreak >=100:
                amount += 250
        fvalue = f"{amount + 5 * (nrstreak - 1)}<:coin:845012771594043412>"
        before = bool(lastdaily.to_dict())
        beforestreak = bool(laststreak.to_dict())
        amountcrates = 0
        if before is True and beforestreak is True:
            then = lastdaily.to_dict()['dailycooldown']
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(86400+then/1e3)
            streakexpire = datetime.datetime.fromtimestamp(172800+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.description = f"You can get your daily rewards again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**"
                return await ctx.send(embed=embed)
            else:
                nrstreak = db.collection(u"streak").document(f"{ctx.author.id}").get().to_dict()['streak']
                db.collection(u"daily").document(f"{ctx.author.id}").set({u'dailycooldown': int(round(time.time() * 1000))})
                if todaydate > streakexpire:
                    db.collection(u"streak").document(f"{ctx.author.id}").set({u'streak': 1})
                    nrstreak = db.collection(u"streak").document(f"{ctx.author.id}").get().to_dict()['streak']
                    embed = discord.Embed(description="Daily Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="Collected ", value=fvalue)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 5*(nrstreak -1))})
                    owned = False
                    if boxchance == 1:
                        embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x1**", inline=False)
                        for x, y in item:
                            if x == crate:
                                owned = True
                                amountcrates = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()['items']['**24.** Loot Crate']
                        if owned == True:
                            db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates + 1}}, merge=True)
                        else:
                            db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: 1}}, merge=True)
                    embed.set_footer(text=f"Daily Streak: {nrstreak}")
                    await ctx.send(embed=embed)
                else:
                    db.collection(u"streak").document(f"{ctx.author.id}").set({u'streak': nrstreak+1})
                    nrstreak = db.collection(u"streak").document(f"{ctx.author.id}").get().to_dict()['streak']
                    embed = discord.Embed(description="Daily Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Collected <:coin:845012771594043412>", value=fvalue)
                    db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 5*(nrstreak -1))})
                    owned = False
                    if boxchance == 1:
                        embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x1**", inline=False)
                        for x, y in item:
                            if x == crate:
                                owned = True
                                amountcrates = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()['items']['**24.** Loot Crate']
                        if owned == True:
                            db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates + 1}}, merge=True)
                        else:
                            db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: 1}}, merge=True)
                    embed.set_footer(text=f"Daily Streak: {nrstreak}")
                    await ctx.send(embed=embed)
        else:
            db.collection(u"daily").document(f"{ctx.author.id}").set({u'dailycooldown': int(round(time.time() * 1000))})
            db.collection(u"streak").document(f"{ctx.author.id}").set({u'streak': 1})
            nrstreak = db.collection(u"streak").document(f"{ctx.author.id}").get().to_dict()['streak']
            embed = discord.Embed(description="Daily Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Collected", value=fvalue)
            db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 5*(nrstreak -1))})
            owned = False
            if boxchance == 1:
                embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x1**", inline=False)
                for x,y in item:
                    if x == crate:
                        owned = True
                        amountcrates = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()['items']['**24.** Loot Crate']
                if owned == True:
                    db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates + 1}}, merge=True)
                else:
                    db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: 1}}, merge=True)
            embed.set_footer(text=f"Daily Streak: {nrstreak}")
            await ctx.send(embed=embed)

    @commands.command(help="Get your weekly reward. Cooldown resets 1week after the last weekly.", usage="weekly")
    async def weekly(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        balance = db.collection("balance").document(f"{ctx.author.id}").get()
        shinybalance = db.collection("shiny").document(f"{ctx.author.id}").get()
        if not balance.exists or not shinybalance.exists:
            createbalance = db.collection("balance").document(f"{ctx.author.id}")
            createbalance.set({
                'coins': 0
            }, merge=True)
            createshiny = db.collection("shiny").document(f"{ctx.author.id}")
            createshiny.set({
                'shiny': 0
            }, merge=True)
            db.collection(u'inventory').document(f"{ctx.author.id}").set({u'items': []},merge=True)
            db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {}},merge=True)
        lastweekly = db.collection(u"weekly").document(f"{ctx.author.id}").get()
        laststreak =  db.collection(u"wstreak").document(f"{ctx.author.id}").get()
        try:
            amountcrates = db.collection(u'items').document(f'{ctx.author.id}').get().to_dict()['items']['**24.** Loot Crate']
            amountcrates += 3
        except Exception as error:
            if isinstance(error, KeyError):
                amountcrates = 3
            else:
                raise error
        crate = '**24.** Loot Crate'
        amount = 150
        pet = await self.getpet(ctx.author.id)
        try:
            nrstreak = db.collection(u"wstreak").document(f"{ctx.author.id}").get().to_dict()['streak']
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection(u"wstreak").document(f"{ctx.author.id}").set({'streak': 1})
        try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
        except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
        if pet == 'Plessie' and lvl == 5 and xp == "MAX LEVEL":
            if nrstreak >=10 and nrstreak <= 49:
                amount += 50
            elif nrstreak >= 50 and nrstreak <= 99:
                amount += 200
            elif nrstreak >= 100:
                amount += 500
        before = bool(lastweekly.to_dict())
        beforestreak = bool(laststreak.to_dict())
        if before is True and beforestreak is True:
            then = lastweekly.to_dict()['weeklycooldown']
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(604800+then/1e3)
            streakexpire = datetime.datetime.fromtimestamp(1209600+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            days = timeleft.days
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.description = f"You can get your weekly rewards again in **{str(days) + 'd ' + str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**"
                return await ctx.send(embed=embed)
            else:
                nrstreak = db.collection(u"wstreak").document(f"{ctx.author.id}").get().to_dict()['streak']
                db.collection(u"weekly").document(f"{ctx.author.id}").set({u'weeklycooldown': int(round(time.time() * 1000))})
                if todaydate > streakexpire:
                    db.collection(u"wstreak").document(f"{ctx.author.id}").set({u'streak': 1})
                    nrstreak = db.collection(u"wstreak").document(f"{ctx.author.id}").get().to_dict()['streak']
                    embed = discord.Embed(description="Weekly Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Collected ", value=f"{amount + 15*(nrstreak - 1)}<:coin:845012771594043412>")
                    embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x3**",inline=False)
                    db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 15*(nrstreak -1))})
                    db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates}}, merge=True)
                    embed.set_footer(text=f"Weekly Streak: {nrstreak}")
                    await ctx.send(embed=embed)
                else:
                    db.collection(u"wstreak").document(f"{ctx.author.id}").set({u'streak': nrstreak+1})
                    nrstreak = db.collection(u"wstreak").document(f"{ctx.author.id}").get().to_dict()['streak']
                    embed = discord.Embed(description="Weekly Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Collected <:coin:845012771594043412>",value=f"{amount + 15*(nrstreak - 1)}<:coin:845012771594043412>")
                    embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x3**",inline=False)
                    db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates}}, merge=True)
                    db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 15*(nrstreak -1))})
                    embed.set_footer(text=f"Weekly Streak: {nrstreak}")
                    await ctx.send(embed=embed)
        else:
            db.collection(u"weekly").document(f"{ctx.author.id}").set({u'weeklycooldown': int(round(time.time() * 1000))})
            db.collection(u"wstreak").document(f"{ctx.author.id}").set({u'streak': 1})
            nrstreak = db.collection(u"wstreak").document(f"{ctx.author.id}").get().to_dict()['streak']
            embed = discord.Embed(description="Weekly Reward", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Collected", value=f"{amount + 15 * (nrstreak - 1)} <:coin:845012771594043412>")
            db.collection('balance').document(f'{ctx.author.id}').set({'coins':db.collection('balance').document(f'{ctx.author.id}').get().to_dict()['coins'] + (amount + 15*(nrstreak -1))})
            embed.add_field(name="Bonus Item:", value="<a:loot_box:913440884018774036>Loot Crate **x3**", inline=False)
            db.collection(u"items").document(f"{ctx.author.id}").set({u'items':{crate: amountcrates}}, merge=True)
            embed.set_footer(text=f"Weekly Streak: {nrstreak}")
            await ctx.send(embed=embed)

    @commands.command(help="Heads or tails. If you guess correctly you can double your money.", usage="coinflip <amount> <choice>",aliases=['cf'])
    async def coinflip(self, ctx, amount: int, userchoice: typing.Optional[str]):
        if ctx.channel.id != 728299872947667106:
            return
        if amount < 1:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```You can't bet an amount lower than 1!```")
            return await ctx.message.reply(embed=embed)
        elif amount > 2000:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be greater than 2000 <:coin:845012771594043412>```")
            return await ctx.message.reply(embed=embed)
        lastcoinflip = db2.collection(u'coinflip').document(f"{ctx.author.id}").get()
        before = bool(lastcoinflip.to_dict())
        pet = await self.getpet(ctx.author.id)
        if before is True:
                then = lastcoinflip.to_dict()['cooldown']
                today = int(round(time.time()*1000))
                todaydate = datetime.datetime.fromtimestamp(today/1e3)
                if pet == 'Bobby':
                    try:
                        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
                    except Exception as error:
                        if isinstance(error,KeyError):
                            lvl = 0
                        xp = "not owned"
                if pet == 'Bobby' and lvl == 5 and xp == "MAX LEVEL":
                    thendate = datetime.datetime.fromtimestamp(300+then/1e3)
                else:
                    thendate = datetime.datetime.fromtimestamp(600+then/1e3)
                timeleft = abs(todaydate-thendate)
                seconds = timeleft.seconds
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                if todaydate < thendate:
                    return await ctx.message.reply(f"You can't coinflip yet! Time Remaining: **{str(minutes) + 'm ' + str(seconds) + 's '}**")
        balance = db.collection("balance").document(f"{ctx.author.id}").get()
        shinybalance = db.collection("shiny").document(f"{ctx.author.id}").get()
        if balance.to_dict()["coins"] < amount:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Amount can't be greater than user's amount of coins!```")
            return await ctx.message.reply(embed=embed)
        choices = ["heads", "tails"]
        if userchoice.lower() not in choices:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error: ", value="```Invalid choice!```")
            return await ctx.message.reply(embed=embed)
        choice = random.choice(choices)
        if userchoice:
            db2.collection(u'coinflip').document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))}, merge=True)
            if userchoice == choice:
                db.collection("balance").document(f"{ctx.author.id}").update({ "coins": balance.to_dict()["coins"] + amount})
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), title=choice.capitalize(),description=f"**{ctx.author.name}**, you got that right!")
                embed.add_field(name="Coins", value=f"{balance.to_dict()['coins'] + amount} <:coin:845012771594043412>")
                embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
                return await ctx.send(embed=embed)
            else:
                if pet == 'Mew':
                    try:
                        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
                    except Exception as error:
                        if isinstance(error,KeyError):
                            lvl = 0
                            xp = "not owned"
                if pet == 'Mew' and lvl == 5 and xp == "MAX LEVEL":
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
                            db.collection("balance").document(f"{ctx.author.id}").update({ "coins": balance.to_dict()["coins"] - amount})
                            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title=choice.capitalize(),description=f"**{ctx.author.name}**, better luck next time.")
                            embed.add_field(name="Coins", value=f"{balance.to_dict()['coins'] - amount} <:coin:845012771594043412>")
                            embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
                            return await ctx.send(embed=embed)
                        else:
                            message = await ctx.message.reply(f"```You want to use the daily Coinflip loss prevention? If not press the ❌ to cancel the command else press the ✅!```")
                            await message.add_reaction('✅')
                            await message.add_reaction('❌')
                            reaction,user = await self.bot.wait_for('reaction_add', check = lambda reaction,user: user == ctx.author and (reaction.emoji == '✅' or reaction.emoji == '❌'))
                            if reaction.emoji == '✅':
                                amount = 0
                                await message.delete()
                                db.collection("balance").document(f"{ctx.author.id}").update({ "coins": balance.to_dict()["coins"] - amount})
                                embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title=choice.capitalize(),description=f"**{ctx.author.name}**, Loss Prevented!")
                                embed.add_field(name="Coins", value=f"{balance.to_dict()['coins'] - amount} <:coin:845012771594043412>")
                                embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
                                db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                                'ability': int(round(time.time() * 1000)),
                                }},merge=True)
                                return await ctx.send(embed=embed)
                            else:
                                await message.delete()
                                db.collection("balance").document(f"{ctx.author.id}").update({ "coins": balance.to_dict()["coins"] - amount})
                                embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title=choice.capitalize(),description=f"**{ctx.author.name}**, better luck next time.")
                                embed.add_field(name="Coins", value=f"{balance.to_dict()['coins'] - amount} <:coin:845012771594043412>")
                                embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
                                return await ctx.send(embed=embed)
                    except Exception as error:
                        if isinstance(error,TypeError):
                            db.collection(u"petinventory").document(f"{ctx.author.id}").set({u'cooldowns': {
                                'ability':int(round(time.time() * 1000)),
                            }},merge=True)
                        else:
                            raise error
                db.collection("balance").document(f"{ctx.author.id}").update({ "coins": balance.to_dict()["coins"] - amount})
                embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title=choice.capitalize(),description=f"**{ctx.author.name}**, better luck next time.")
                embed.add_field(name="Coins", value=f"{balance.to_dict()['coins'] - amount} <:coin:845012771594043412>")
                embed.add_field(name="Shiny rupees", value=f"{shinybalance.to_dict()['shiny']} <:1_shiny_rupee:755974674927845456>")
                return await ctx.send(embed=embed)

    def fish_cooldown(self,fisher_id):
        lastfish = db2.collection(u'fish').document(f"{fisher_id}").get()
        pet = self._getpet(fisher_id)
        try:
            before = lastfish.to_dict()
            if before is None:
                raise TypeError
            else:
                then = lastfish.to_dict()[u'cooldown']
                today = int(round(time.time()*1000))
                todaydate = datetime.datetime.fromtimestamp(today/1e3)
                try:
                    lvl = db.collection('petinventory').document(f'{fisher_id}').get().to_dict()['pets'][pet]['Level']
                    xp = db.collection('petinventory').document(f'{fisher_id}').get().to_dict()['pets'][pet]['XP']
                except Exception as error:
                    if isinstance(error,KeyError):
                        lvl = 0
                        xp = "not owned"
                if pet == 'Snom' and lvl == 5 and xp=="MAX LEVEL":
                    thendate = datetime.datetime.fromtimestamp(10+then/1e3)
                else:
                    thendate = datetime.datetime.fromtimestamp(25+then/1e3)
                timeleft = abs(todaydate-thendate)
                seconds = timeleft.seconds
                seconds = seconds % 60
                if todaydate < thendate:
                    return seconds
                db2.collection(u"fish").document(f"{fisher_id}").set({u'cooldown': int(round(time.time() * 1000))})
                return "no cooldown"
        except Exception as error:
            if isinstance(error, TypeError):
                db2.collection(u"fish").document(f"{fisher_id}").set({u'cooldown': int(round(time.time() * 1000))})
                return "no cooldown"
            else:
                raise error

    @staticmethod
    def fish_inv(fisher: discord.Member):
        try:
            fishinv = db.collection(u"fishinv").document(f"{fisher.id}").get().to_dict()["inv"]
            if fishinv is None:
                raise TypeError
            fishinv = {
                "Common Fish <:cheep_cheep:752019412705607700>": fishinv["Common Fish"],
                "Uncommon Fish <:cheep_deep:752018862509260841>": fishinv["Uncommon Fish"],
                "Rare Fish <:cheep_bleep:752019942945194006>": fishinv["Rare Fish"],
                "Legendary Fish <:cheep_eep:752019232643874827>": fishinv["Legendary Fish"],
                "Unlucky Reels <:unagi:752018506173907034><:cheep_chomp:752018755927670804><:blooper:752018973335486543><:porcupuffer:752018538675437638><:komboo:752018418349113364><:bone_fish:752018827033706547>": fishinv["Unlucky Reels"]
            }
        except Exception as error:
            if isinstance(error, TypeError):
                fishinv = {
                    'inv': 
                    {
                    "Common Fish <:cheep_cheep:752019412705607700>": 0,
                    "Uncommon Fish <:cheep_deep:752018862509260841>": 0,
                    "Rare Fish <:cheep_bleep:752019942945194006>": 0,
                    "Legendary Fish <:cheep_eep:752019232643874827>": 0,
                    "Unlucky Reels <:unagi:752018506173907034><:cheep_chomp:752018755927670804><:blooper:752018973335486543><:porcupuffer:752018538675437638><:komboo:752018418349113364><:bone_fish:752018827033706547>": 0
                    }
                }
                db.collection(u"fishinv").document(f"{fisher.id}").set(fishinv, merge=True)
                string = ""
                for k, v in fishinv['inv'].items():
                    string += f"{k}: {v}\n"
                embed = discord.Embed(color=discord.Color.gold(), description=string)
                embed.set_author(name=f"{fisher.name}'s fishing stats", icon_url=fisher.avatar_url)
                return embed
            else:
                raise error
        string = ""
        for k, v in fishinv.items():
            string += f"{k}: {v}\n"
        embed = discord.Embed(color=discord.Color.gold(), description=string)
        embed.set_author(name=f"{fisher.name}'s fishing stats", icon_url=fisher.avatar_url)
        return embed

    def fish_function(self,fisher: discord.Member):
        try:
            bal = db.collection("balance").document(f"{fisher.id}").get().to_dict()['coins']
            db.collection("balance").document(f"{fisher.id}").update({
                'coins': bal - 10
            })
        except Exception as error:
            if isinstance(error, TypeError):
                createbalance = db.collection("balance").document(f"{fisher.id}")
                createbalance.set({
                    'coins': 0
                }, merge=True)
                createshiny = db.collection("shiny").document(f"{fisher.id}")
                createshiny.set({
                    'shiny': 0
                }, merge=True)
                return "***You don't have enough money to fish.***"
            else:
                raise error
        fishes = {
            "crate": ("Loot Crate", None, "<a:loot_box:913440884018774036>", "**24.** Loot Crate"),
            "unagi": ("Unagi", -1000, "<:unagi:752018506173907034>", "Unlucky Reels", "I SURVIVED UNAGI"),
            "chomp": ("Cheep Chomp", -5, "<:cheep_chomp:752018755927670804>", "Unlucky Reels"),
            "blooper": ("Blooper", -5, "<:blooper:752018973335486543>", "Unlucky Reels"),
            "puffer": ("Porcupuffer", -5, "<:porcupuffer:752018538675437638>", "Unlucky Reels"),
            "komboo": ("Komboo", 5, "<:komboo:752018418349113364>", "Unlucky Reels"),
            "urchin": ("Urchin", 5, "<:urchin:752018578349228032>", "Unlucky Reels"),
            "bone": ("Bone Fish", 5, "<:bone_fish:752018827033706547>", "Unlucky Reels"),
            "cheep": ("Cheep Cheep", 15, "<:cheep_cheep:752019412705607700>", "Common Fish"),
            "deep": ("Deep Cheep", 25, "<:cheep_deep:752018862509260841>", "Uncommon Fish"),
            "bleep": ("Snow Cheep", 40, "<:cheep_bleep:752019942945194006>", "Rare Fish"),
            "eep": ("Eep Cheep", 2500, "<:cheep_eep:752019232643874827>", "Legendary Fish", "〈 🎣 〉")
        }

        fishes_to_get = [
            "unagi",
            "eep",
            "crate",
            "bleep",
            random.choice(["puffer", "blooper", "chomp"]),
            random.choice(["bone", "urchin", "komboo"]),
            "deep",
            "cheep",
            random.choice(["unagi", "eep", "crate", "bleep", random.choice(["puffer", "blooper", "chomp"]), random.choice(["bone", "urchin", "komboo"]), "deep", "cheep"])
        ]
        try:
            bait = db.collection("items").document(f"{fisher.id}").get().to_dict()["items"]["**26.** Fish Bait"]
            probabilities = [2/1000, 8/1000, 30/1000, 60/1000, 200/1000, 300/1000, 150/1000, 250/1000, 0/1000]
            if bait - 1 == 0:
                db.collection("items").document(f"{fisher.id}").set({
                    "items": {
                        "**26.** Fish Bait": firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("items").document(f"{fisher.id}").set({
                    "items": {
                        "**26.** Fish Bait": bait - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                probabilities = [1/1000, 2/1000, 30/1000, 50/1000, 100/1000, 250/1000, 200/1000, 347/1000, 20/1000]
            elif isinstance(error, TypeError):
                probabilities = [1/1000, 2/1000, 30/1000, 50/1000, 100/1000, 250/1000, 200/1000, 347/1000, 20/1000]
        pet = self._getpet(fisher.id)
        item_caught2 = [None,None,None,None]
        if pet == 'Judd':
            try:
                    lvl = db.collection('petinventory').document(f'{fisher.id}').get().to_dict()['pets'][pet]['Level']
                    xp = db.collection('petinventory').document(f'{fisher.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                    if isinstance(error,KeyError):
                        lvl = 0
                        xp = "not owned"
        if pet == 'Judd' and lvl == 5 and xp == "MAX LEVEL":
            fishchance = random.choices(["yes", "no"], weights=[20, 80], k=1)[0]
            if fishchance == "yes":
                item_caught = random.choices(fishes_to_get, weights=probabilities, k=1)
                item_caught = fishes[item_caught[0]]
                item_caught2 = random.choices(fishes_to_get, weights=probabilities, k=1)
                item_caught2 = fishes[item_caught2[0]]
            else:
                item_caught = random.choices(fishes_to_get, weights=probabilities, k=1)
                item_caught = fishes[item_caught[0]]
        else:
            item_caught = random.choices(fishes_to_get, weights=probabilities, k=1)
            item_caught = fishes[item_caught[0]]

        result_list = [None, None]

        if item_caught[0] == "Unagi":
            result_list[1] = item_caught[4]
        if item_caught2[0] == 'Unagi':
            result_list[1] = item_caught2[4]
        elif item_caught[0] == "Unagi" and item_caught2[0] == "Unagi":
            result_list[1] = item_caught[4]
        
        if item_caught[0] == "Eep Cheep" and item_caught2 == "Eep Cheep":
            try:
                eeps = db.collection("eep").document(f"{fisher.id}").get().to_dict()["eep"]
                db.collection("eep").document(f"{fisher.id}").update({
                    "eep": eeps + 2
                })
            except Exception as error:
                if isinstance(error, TypeError):
                    db.collection("eep").document(f"{fisher.id}").set({
                        "eep": 2
                    })
                else:
                    raise error
            result_list[1] = item_caught[4]

        if item_caught[0] == "Eep Cheep":
            try:
                eeps = db.collection("eep").document(f"{fisher.id}").get().to_dict()["eep"]
                db.collection("eep").document(f"{fisher.id}").update({
                    "eep": eeps + 1
                })
            except Exception as error:
                if isinstance(error, TypeError):
                    db.collection("eep").document(f"{fisher.id}").set({
                        "eep": 1
                    })
                else:
                    raise error
            result_list[1] = item_caught[4]
            
        if item_caught2[0] == "Eep Cheep":
            try:
                eeps = db.collection("eep").document(f"{fisher.id}").get().to_dict()["eep"]
                db.collection("eep").document(f"{fisher.id}").update({
                    "eep": eeps + 1
                })
            except Exception as error:
                if isinstance(error, TypeError):
                    db.collection("eep").document(f"{fisher.id}").set({
                        "eep": 1
                    })
                else:
                    raise error
            result_list[1] = item_caught2[4]

        if item_caught[0] == "Loot Crate" and item_caught2[0] == "Loot Crate":
            try:
                crates = db.collection(u"items").document(f"{fisher.id}").get().to_dict()['items'][item_caught[3]]
                db.collection(u"items").document(f"{fisher.id}").set({
                    'items': {
                        item_caught[3]: crates + 2
                    }
                }, merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection(u"items").document(f"{fisher.id}").set({
                        'items': {
                            item_caught[3]: 2
                        }
                    }, merge=True)
                else:
                    raise error
            embed = discord.Embed(
                description=f"Guess it's your lucky day.\n**🎣  |  you caught:** x2 {item_caught[2]} {item_caught[0]}",
                color=discord.Color.gold()
            )
            embed.set_author(name=fisher.name, icon_url=fisher.avatar_url)
            result_list[0] = embed
            return result_list
        
        if item_caught[0] == "Loot Crate":
            try:
                crates = db.collection(u"items").document(f"{fisher.id}").get().to_dict()['items'][item_caught[3]]
                db.collection(u"items").document(f"{fisher.id}").set({
                    'items': {
                        item_caught[3]: crates + 1
                    }
                }, merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection(u"items").document(f"{fisher.id}").set({
                        'items': {
                            item_caught[3]: 1
                        }
                    }, merge=True)
                else:
                    raise error
            embed = discord.Embed(
                description=f"Guess it's your lucky day.\n**🎣  |  you caught:** {item_caught[2]} {item_caught[0]}",
                color=discord.Color.gold()
            )
            embed.set_author(name=fisher.name, icon_url=fisher.avatar_url)
            result_list[0] = embed
            return result_list

        if item_caught2[0] == "Loot Crate":
            try:
                crates = db.collection(u"items").document(f"{fisher.id}").get().to_dict()['items'][item_caught[3]]
                db.collection(u"items").document(f"{fisher.id}").set({
                    'items': {
                        item_caught2[3]: crates + 1
                    }
                }, merge=True)
            except Exception as error:
                if isinstance(error, KeyError):
                    db.collection(u"items").document(f"{fisher.id}").set({
                        'items': {
                            item_caught2[3]: 1
                        }
                    }, merge=True)
                else:
                    raise error
            embed = discord.Embed(
                description=f"Guess it's your lucky day.\n**🎣  |  you caught:** {item_caught2[2]} {item_caught2[0]}",
                color=discord.Color.gold()
            )
            result_list[0] = embed
            return result_list
        

        try:
            reels = db.collection(u"fishinv").document(f"{fisher.id}").get().to_dict()["inv"]
            fishinv = {
                    "Common Fish": reels["Common Fish"],
                    "Uncommon Fish": reels["Uncommon Fish"],
                    "Rare Fish": reels["Rare Fish"],
                    "Legendary Fish": reels["Legendary Fish"],
                    "Unlucky Reels": reels["Unlucky Reels"]
                }
            fishinv[item_caught[3]] += 1
            if item_caught2[3] is not None:
                fishinv[item_caught2[3]] += 1
            db.collection(u"fishinv").document(f"{fisher.id}").set({
                "inv": fishinv
            }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                fishinv = {
                    "Common Fish": 0,
                    "Uncommon Fish": 0,
                    "Rare Fish": 0,
                    "Legendary Fish": 0,
                    "Unlucky Reels": 0
                }
                fishinv[item_caught[3]] = 1
                if item_caught2[3] is not None:
                    fishinv[item_caught2[3]] = 1
                db.collection(u"fishinv").document(f"{fisher.id}").set({
                    "inv": fishinv
                }, merge=True)
            else:
                raise error

        if item_caught2[1] is not None and item_caught[1] + item_caught2[1] < 0:
            string = f"you lost {(item_caught2[1] + item_caught[1]) * -1} coins."
        elif item_caught2[1] is not None and item_caught[1] + item_caught2[1] >= 0:
            string = f"sold them for {item_caught[1] + item_caught2[1]} coins."
        elif item_caught2[1] is None and item_caught[1] < 0:
            string = f"you lost {item_caught[1] * -1} coins."
        else:
            string = f"sold it for {item_caught[1]} coins."
        if item_caught2[2] is not None and item_caught2[0] is not None:
            embed = discord.Embed(
                color=discord.Color.gold(),
                description=f"**🎣  |  you caught:** {item_caught[2]} {item_caught[0]}, {item_caught2[2]} {item_caught2[0]} and {string}"
            )
            embed.set_author(name=fisher.name, icon_url=fisher.avatar_url)
        else:
            embed = discord.Embed(
                color=discord.Color.gold(),
                description=f"**🎣  |  you caught:** {item_caught[2]} {item_caught[0]} and {string}"
            )
            embed.set_author(name=fisher.name, icon_url=fisher.avatar_url)
        try:
                lvl = db.collection('petinventory').document(f'{fisher.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{fisher.id}').get().to_dict()['pets'][pet]['XP']
        except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
        if pet == 'Korok' and lvl == 5 and xp == "MAX LEVEL":
            bal += 10
        if item_caught2[1] is not None and bal - 10 + item_caught[1] + item_caught2[1] <= 0:
            embed.description += " You are broke now :("
            bal = 0
        else:
            bal = bal - 10 + item_caught[1]
        db.collection("balance").document(f"{fisher.id}").update({
                'coins': bal
            })
        result_list[0] = embed
        return result_list

    @commands.group(help="Try your luck and fish.", usage="fish <stats> (optional)", case_insensitive=True)
    async def fish(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.channel.id != 728299872947667106:
                return
            balance = db.collection("balance").document(f"{ctx.author.id}").get()
            shinybalance = db.collection("shiny").document(f"{ctx.author.id}").get()
            if not balance.exists or not shinybalance.exists:
                createbalance = db.collection("balance").document(f"{ctx.author.id}")
                createbalance.set({
                    'coins': 0
                }, merge=True)
                createshiny = db.collection("shiny").document(f"{ctx.author.id}")
                createshiny.set({
                    'shiny': 0
                }, merge=True)
                db.collection(u'inventory').document(f"{ctx.author.id}").set({u'items': []},merge=True)
                db.collection(u'items').document(f"{ctx.author.id}").set({u'items': {}},merge=True)
            thread_pool = ThreadPoolExecutor(max_workers=1)
            partial_cooldown = partial(self.fish_cooldown, ctx.author.id)
            bal = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()['coins']
            if bal - 10 < 0:
                return await ctx.message.reply("***You don't have enough money to fish.***")
            cooldown = await self.bot.loop.run_in_executor(thread_pool, partial_cooldown)
            if type(cooldown) is int:
                raise commands.CommandOnCooldown(cooldown=25, retry_after=cooldown)
            partial_fish = partial(self.fish_function, ctx.author)
            result = await self.bot.loop.run_in_executor(thread_pool, partial_fish)
            if type(result[0]) is str:
                await ctx.message.reply(result)
            else:
                await ctx.send(embed=result[0])
            if result[1] is not None:
                role = discord.utils.get(ctx.guild.roles, name=result[1])
                await ctx.author.add_roles(role)

    @fish.command(help="Shows your's or someone else's fishing stats.", usage="fish stats @user (optional)")
    async def stats(self, ctx, member: discord.Member = None):
        if ctx.channel.id != 728299872947667106:
            return
        if member is None:
            member = ctx.author
        thread_pool = ThreadPoolExecutor()
        partial_inv = partial(self.fish_inv, member)
        embed = await self.bot.loop.run_in_executor(thread_pool, partial_inv)
        await ctx.send(embed=embed)

    @commands.group(help="Support the bot and get benefits through Patreon.", usage="patreon", aliases=["patron"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def patreon(self,ctx):
        if ctx.invoked_subcommand is None:
            if ctx.channel.id != 728299872947667106:
                return
            embed = discord.Embed(
                title="Patreon Link", url="https://www.patreon.com/nskbot",
                timestamp=datetime.datetime.utcnow(),
                color=0xff6347
            )
            embed.add_field(name="Tier 1",value="```fix\n1. Patron Role\n2. 10K Coins\n3. 2 Shiny Rupees\n```[Link](https://www.patreon.com/join/nskbot/checkout?rid=7259353)",inline=False)
            embed.add_field(name="Tier 2",value="```fix\n1. Patron Role\n2. 20K Coins\n3. 5 Shiny Rupees\n```[Link](https://www.patreon.com/join/nskbot/checkout?rid=7259372)",inline=False)
            embed.add_field(name="Tier 3",value="```fix\n1. Patron Role\n2. 30K Coins\n3. 10 Shiny Rupees\n4. 1 Rare Pet\n```[Link](https://www.patreon.com/join/nskbot/checkout?rid=7259382)",inline=False)
            embed.add_field(name="Early Access",value="```fix\n1. Patron Role\n2. Bot Tester Role\n3. 30k Coins\n4. 10 Shiny Rupees\n5. Bot Tester Pet\n```[Link](https://www.patreon.com/join/nskbot/checkout?rid=7259394)",inline=False)
            embed.add_field(name="Tier 4",value="```fix\n1. Patron Role\n2. 50k Coins\n3. 25 Shiny Rupees\n4. 1 Legendary Pet and 1 Custom Pet (with special ability)\n```[Link](https://www.patreon.com/join/nskbot/checkout?rid=7259401)",inline=False)
            embed.set_author(name="NSK Bot", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/832685967898705960/849885544737538048/patreon-creators-patreon.png")
            embed.set_footer(icon_url=self.bot.user.avatar_url, text=f"Use <{ctx.prefix}patreon claim> to get your currency benefits according to your tier.")
            await ctx.send(embed=embed)
    
    @patreon.command(help="Claim your bot patron benefits according to your tier.", usage="patreon claim")
    @commands.cooldown(2629743, 2, commands.BucketType.user)
    async def claim(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        benefits = {
            "Patron Tier 1": [10000, 2, None, None],
            "Patron Tier 2": [20000, 5, None, None],
            "Patron Tier 3": [30000, 10, "<insert rare pet>", None],
            "Patron Early Access": [30000, 10, "<insert tester pet>", None],
            "Patron Tier 4": [50000, 25, "<insert legendary pet>", "<insert custom pet>"]
        }
        tier_roles = ["Patron Tier 1", "Patron Tier 2", "Patron Tier 3", "Patron Early Access", "Patron Tier 4"]
        valid = False
        for role_name in tier_roles:
            role = discord.utils.get(ctx.author.roles, name=role_name)
            if role is not None:
                valid = True
                benefit = benefits[role_name]
                break
        if valid is False:
            embed = discord.Embed(description="You are not a bot supporter :(", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        else:
            try:
                lastclaim = db2.collection('patreon').document(f'{ctx.author.id}').get().to_dict()['cd']
                then = lastclaim
                today = int(round(time.time()*1000))
                todaydate = datetime.datetime.fromtimestamp(today/1e3)
                thendate = datetime.datetime.fromtimestamp(2629743+then/1e3)
                timeleft = abs(todaydate-thendate)
                seconds = timeleft.seconds
                days = timeleft.days
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                if todaydate < thendate:
                    return await ctx.message.reply(f"You can claim your patron rewards in **{str(days) +'d ' +str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
                db.collection(u"patreon").document(f"{ctx.author.id}").set({'cd': int(round(time.time() * 1000))},merge=True)
            except Exception as error:
                if isinstance(error,TypeError):
                    db.collection(u"patreon").document(f"{ctx.author.id}").set({'cd': int(round(time.time() * 1000))},merge=True)
                else:
                    raise error
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description="Successfully claimed patron rewards! Thank you for supporting the bot <3")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        try:
            coins = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
            db.collection("balance").document(f"{ctx.author.id}").set({
                "coins": coins + benefit[0]
            }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection("balance").document(f"{ctx.author.id}").set({
                    "coins": benefit[0]
                }, merge=True)
            elif isinstance(error, KeyError):
                db.collection("balance").document(f"{ctx.author.id}").set({
                    "coins": benefit[0]
                }, merge=True)
            else:
                raise error
        embed.add_field(name="Coins", value=str(benefit[0]) + '<:coin:845012771594043412>')

        try:
            shiny = db.collection("shiny").document(f"{ctx.author.id}").get().to_dict()["shiny"]
            db.collection("shiny").document(f"{ctx.author.id}").set({
                "shiny": shiny + benefit[1]
            }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection("shiny").document(f"{ctx.author.id}").set({
                    "shiny": benefit[1]
                }, merge=True)
            elif isinstance(error, KeyError):
                db.collection("shiny").document(f"{ctx.author.id}").set({
                    "shiny": benefit[1]
                }, merge=True)
            else:
                raise error
        embed.add_field(name="Shiny Rupees", value=str(benefit[1]) + '<:1_shiny_rupee:755974674927845456>', inline=False)

        if role.name == "Patron Tier 3" or role.name == "Patron Tier 4":
            check = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()
            if check is None:
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
                },merge=True)
                if role.name == "Patron Tier 3":
                    rarepets = ['Baby Yoshi', 'Plessie', 'Korok', 'Boo Guy', 'K. K. Slider']
                    _rarepets = random.choices(rarepets, weights=[5,5,5,5,5], k = 1)[0]
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                            'pets': {
                                _rarepets:{
                                    'Level': 1,
                                    'XP': 0,
                                    'rarity': 'Rare'
                                }
                            }
                        },merge=True)
                    embed.add_field(name="Rare Pet", value=_rarepets, inline=False)
                else:
                    legendarypets = ['Terrako', 'Polterpup', 'Judd', 'Bobby', 'Mew']
                    _legendarypets = random.choices(legendarypets, weights=[5,5,5,5,5], k = 1)[0]
                    db.collection('petinventory').document(f'{ctx.author.id}').set({
                            'pets': {
                                _legendarypets:{
                                    'Level': 1,
                                    'XP': 0,
                                    'rarity': 'Legendary'
                                }
                            }
                        },merge=True)
                    embed.add_field(name="Legendary Pet", value=_legendarypets)
                    embed.add_field(name="Custom Pet", value="Contact <@465138950223167499> and <@449555448010375201>", inline=False)
            else:
                if role.name == "Patron Tier 3":
                    rarepets = ['Baby Yoshi', 'Plessie', 'Korok', 'Boo Guy', 'K. K. Slider']
                    _rarepets = random.choices(rarepets, weights=[5,5,5,5,5], k = 1)[0]
                    embed.add_field(name="Rare Pet", value=_rarepets, inline=False)
                    if _rarepets in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
                        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][_rarepets]['Level']
                        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][_rarepets]['XP']
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
                                    _rarepets: {
                                        'Level': lvl +1,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _rarepets: {
                                        'XP': xp + 1120
                                    }
                                }
                            },merge=True)
                        elif lvl == 1:
                            amount = 1120 - (xpcap - xp + 700)
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _rarepets: {
                                        'Level': lvl + 2,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif lvl == 2:
                            amount = 1120 - (xpcap - xp)
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _rarepets: {
                                        'Level': lvl + 1,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif lvl == 5 and xp + 1120 > xpcap:
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _rarepets: {
                                        'XP': 'MAX LEVEL'
                                    }
                                }
                            },merge=True)
                else:
                    legendarypets = ['Terrako', 'Polterpup', 'Judd', 'Bobby', 'Mew']
                    _legendarypets = random.choices(legendarypets, weights=[5,5,5,5,5], k = 1)[0]
                    embed.add_field(name="Legendary Pet", value=_legendarypets, inline=False)
                    embed.add_field(name="Custom Pet", value="Contact <@465138950223167499> and <@449555448010375201>", inline=False)
                    if _legendarypets in db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets']:
                        lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][_legendarypets]['Level']
                        xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][_legendarypets]['XP']
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
                                    _legendarypets: {
                                        'Level': lvl +1,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif xp + 1120 < xpcap and lvl != 5 and lvl > 2:
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _legendarypets: {
                                        'XP': xp + 1120
                                    }
                                }
                            },merge=True)
                        elif lvl == 1:
                            amount = 1120 - (xpcap - xp + 700)
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _legendarypets: {
                                        'Level': lvl + 2,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif lvl == 2:
                            amount = 1120 - (xpcap - xp)
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _legendarypets: {
                                        'Level': lvl + 1,
                                        'XP': amount
                                    }
                                }
                            },merge=True)
                        elif lvl == 5 and xp + 1120 > xpcap:
                            db.collection('petinventory').document(f'{ctx.author.id}').set({
                                'pets':{
                                    _legendarypets: {
                                        'XP': 'MAX LEVEL'
                                    }
                                }
                            },merge=True)
                
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
