import discord
from discord.ext import commands
from firebase_admin import firestore
import datetime
import random
import json
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from dpymenus import PaginatedMenu, Page
import firebase_admin
import typing
import time

db = firestore.client(firebase_admin._apps['maindb'])
db2 = firestore.client(firebase_admin._apps['extra-database'])

class Cooking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.plates = {
            "carrotcake": "Carrot Cake",
            "carrotstew": "Carrot Stew",
            "creamofmushroomsoup": "Cream of Mushroom Soup", "mushroomsoup": "Cream of Mushroom Soup",
            "creamofvegetablesoup": "Cream of Vegetable Soup", "creamvegetablesoup": "Cream of Vegetable Soup", "vegetablesoup": "Cream of Vegetable Soup",
            "creamyheartsoup": "Creamy Heart Soup", "heartsoup": "Creamy Heart Soup",
            "creamymeatsoup": "Creamy Meat Soup", "meatsoup": "Creamy Meat Soup",
            "creamyseafoodsoup": "Creamy Seafood Soup", "seafoodsoup": "Creamy Seafood Soup",
            "currypilaf": "Curry Pilaf",
            "curryrice": "Curry Rice",
            "eggpudding": "Egg Pudding",
            "fragrantmushroomsaute": "Fragrant Mushroom Sauté", "mushroomsaute": "Fragrant Mushroom Sauté", "fragrantsaute": "Fragrant Mushroom Sauté", "fragrantmushroomsauté": "Fragrant Mushroom Sauté",
            "fishpie": "Fish Pie",
            "eggtart": "Egg Tart",
            "glazedmeat": "Glazed Meat",
            "glazedmushrooms": "Glazed Mushrooms",
            "friedwildgreens": "Fried Wild Greens", "friedgreens": "Fried Wild Greens", "wildgreens": "Fried Wild Greens",
            "friedeggandrice": "Fried Egg and Rice", "eggandrice": "Fried Egg and Rice", "eggrice": "Fried Egg and Rice", "friedeggrice": "Fried Egg and Rice",
            "fruitpie": "Fruit Pie",
            "fruitandmushroommix": "Fruit and Mushroom Mix", "fruitmushroom": "Fruit and Mushroom Mix", "fruitandmushroom": "Fruit and Mushroom Mix", "fruitmushroommix": "Fruit and Mushroom Mix",
            "friedbananas": "Fried Bananas",
            "gourmetpoultrypilaf": "Gourmet Poultry Pilaf", "poultrypilaf": "Gourmet Poultry Pilaf",
            "gourmetpoultrypcurry": "Gourmet Poultry Curry", "poultrycurry": "Gourmet Poultry Curry",
            "gourmetmeatstew": "Gourmet Meat Stew",
            "gourmetmeatandseafood": "Gourmet Meat and Seafood Fry", "meatandseafood": "Gourmet Meat and Seafood Fry",
            "honeycandy": "Honey Candy",
            "honeycrepe": "Honey Crepe",
            "honeyedapples": "Honeyed Apples",
            "hotbutteredapples": "Hot Buttered Apples", "butteredapples": "Hot Buttered Apples",
            "honeyedfruits": "Honeyed Fruits",
            "meatcurry": "Meat Curry",
            "meatpie": "Meat Pie",
            "meatstew": "Meat Stew",
            "meat-stuffedpumpkin": "Meat-stuffed Pumpkin", "meatstuffedpumpkin": "Meat-stuffed Pumpkin", "stuffedpumpkin": "Meat-stuffed Pumpkin",
            "meatyriceballs": "Meaty Rice Balls", "meatyrice": "Meaty Rice Balls",
            "mushroomriceballs": "Mushroom Rice Balls", "mushroomrice": "Mushroom Rice Balls",
            "mushroomomelet": "Mushroom Omelet",
            "mushroomrisotto": "Mushroom Risotto",
            "eggomelet": "Egg Omelet",
            "peppersteak": "Pepper Steak",
            "plaincrepe": "Plain Crepe",
            "primepoultrypilaf": "Prime Poultry Pilaf",
            "primepoultrycurry": "Prime Poultry Curry",
            "primemeatstew": "Prime Meat Stew",
            "primemeatcurry": "Prime Meat Curry",
            "meatandseafoodfry": "Meat and Seafood Fry", "meatseafoodfry": "Meat and Seafood Fry",
            "pumpkinstew": "Pumpkin Stew",
            "pumpkinpie": "Pumpkin Pie",
            "fruitcake": "Fruit Cake",
            "salmonmeuniere": "Salmon Meunière",
            "salmon meuniere": "Salmon Meunière",
            "salmonmeunière": "Salmon Meunière",
            "salmon meunière": "Salmon Meunière",
            "salmon": "Salmon Meunière",
            "meuniere": "Salmon Meunière",
            "meunière": "Salmon Meunière",
            "monstercake": "Monster Cake"
        }
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
    alias = "Cooking"

    async def getpet(self, user):
        pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
        return pet
    @commands.command(help="See your unlocked food recipes.", usage="cookbook")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cookbook(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        try:
            cookbook = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Cook Book']
            if cookbook is True:
                pass
            else:
                return await ctx.message.reply(f"You don't own a cookbook! Use `{ctx.prefix}pbuy cookbook` to buy one!")
        except Exception as error:
            if isinstance(error, TypeError):
                return await ctx.message.reply("***Use `!setup` to set up your pet inventory***")
            else:
                raise error
        try:
            recipes = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()["cookbook"]
            if recipes == {}:
                embed = discord.Embed(color=discord.Color.gold(), description="You haven't unlocked any recipes yet. Hunt and cook more.", timestamp=datetime.datetime.utcnow())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            with open("./plates.json") as f:
                plates = json.load(f)
            page_list = []
            recipes = list(recipes.keys())
            menu = PaginatedMenu(ctx)
            menu.set_timeout(120)
            for recipe in recipes:
                page = Page(title=recipe, color=discord.Color.gold())
                page.set_author(name=f"{ctx.author.name}'s CookBook", icon_url=ctx.author.avatar_url)
                page.set_thumbnail(url=plates[recipe]["image"])
                page.add_field(name="Ingredient", value="\n".join(list(map(lambda ingr: ingr[1], plates[recipe]["ingredients"]))), inline=False)
                page.add_field(name="Quantity", value="\n".join(list(map(lambda ingr: str(ingr[2]), plates[recipe]["ingredients"]))), inline=False)
                page.add_field(name="Rarity", value="\n".join(list(map(lambda ingr: ingr[0], plates[recipe]["ingredients"]))), inline=False)
                page.add_field(name="Category", value="\n".join(list(map(lambda ingr: ingr[3], plates[recipe]["ingredients"]))), inline=False)
                page_list.append(page)
            menu.add_pages(page_list)
            await menu.open()
        except Exception as error:
            if isinstance(error, TypeError):
                await ctx.message.reply("***Use `!setup` to set up your pet inventory***")
            else:
                raise error

    @staticmethod
    def sell_plate(user: discord.Member, plate_name: str):
        try:
            dish_count = db.collection("petinventory").document(f"{user.id}").get().to_dict()["dishes"][plate_name]
            if dish_count - 1 == 0:
                db.collection("petinventory").document(f"{user.id}").set({
                    "dishes": {
                        plate_name: firestore.DELETE_FIELD
                    }
                }, merge=True)
            else:
                db.collection("petinventory").document(f"{user.id}").set({
                    "dishes": {
                        plate_name: dish_count - 1
                    }
                }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                return "***You don't own that plate!***"
            elif isinstance(error, KeyError):
                return "***You don't own that plate!***"
            else:
                raise error
        with open("./plates.json") as f:
            plate = json.load(f)
            plate = plate[plate_name]
        try:
            balance = db.collection("balance").document(f"{user.id}").get().to_dict()["coins"]
            db.collection("balance").document(f"{user.id}").set({
                "coins": balance + plate["price"]
            }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                db.collection("balance").document(f"{user.id}").set({
                    "coins": plate["price"]
                }, merge=True)
            elif isinstance(error, TypeError):
                db.collection("balance").document(f"{user.id}").set({
                    "coins": plate["price"]
                }, merge=True)
            else:
                raise error
        embed = discord.Embed(color=discord.Color.gold(), description=f"Succesfully sold `{plate_name}` for **{plate['price']}**<:coin:845012771594043412>", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=plate["image"])
        return embed

    @staticmethod
    def cook_plate(user: discord.Member, plate_name: str):
        try:
            cookbook = db.collection('petinventory').document(f'{user.id}').get().to_dict()['cookbook']
        except Exception as error:
            if isinstance(error, KeyError):
                return "***Use `!setup` to set up your pet inventory***"
            elif isinstance(error, TypeError):
                return "***Use `!setup` to set up your pet inventory***"
            else:
                raise error
        try:
            owned_plate = db.collection("petinventory").document(f"{user.id}").get().to_dict()["cookbook"][plate_name]
        except Exception as error:
            if isinstance(error, KeyError):
                return "***You haven't discovered the recipe for this dish yet!***"
            else:
                raise error
        try:
            user_ingredients = db.collection("petinventory").document(f"{user.id}").get().to_dict()["ingredients"]
            with open("./plates.json") as f:
                plate = json.load(f)
                plate = plate[plate_name]
            for ingr in plate["ingredients"]:
                if user_ingredients[ingr[0]][ingr[1]] - ingr[2] < 0:
                    return "***You don't have enough ingredients!***"
            for ingr in plate["ingredients"]:
                if user_ingredients[ingr[0]][ingr[1]] - ingr[2] == 0:
                    db.collection("petinventory").document(f"{user.id}").set({
                        "ingredients": {
                                ingr[0]: {
                                ingr[1]: firestore.DELETE_FIELD
                            }
                        }
                    }, merge=True)
                else:
                    db.collection("petinventory").document(f"{user.id}").set({
                        "ingredients": {
                                ingr[0]: {
                                ingr[1]: user_ingredients[ingr[0]][ingr[1]] - ingr[2]
                            }
                        }
                    }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                return "***You don't have enough ingredients!***"
            elif isinstance(error, KeyError):
                return "***You don't have enough ingredients!***"
            else:
                raise error
        try:
            dish_count = db.collection("petinventory").document(f"{user.id}").get().to_dict()["dishes"][plate_name]
            db.collection("petinventory").document(f"{user.id}").set({
                "dishes": {
                    plate_name: dish_count + 1
                }
            }, merge=True)
        except Exception as error:
            if isinstance(error, KeyError):
                db.collection("petinventory").document(f"{user.id}").set({
                    "dishes": {
                        plate_name: 1
                    }
                }, merge=True)
            else:
                raise error
        embed = discord.Embed(color=discord.Color.gold(), description=f"Succesfully cooked `{plate_name}`", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=plate["image"])
        return embed

    @commands.group(
        help="Cook some delicious food using the ingredients you gathered while hunting. The more ingredients you have, the more recipes you unlock.",
        usage="cook <plate> (optional - in case you unlocked the recipe for that plate)", case_insensitive=True
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cook(self, ctx, *, plate: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        if plate is None:
            try:
                cookbook = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['items']['Cook Book']
                if cookbook is True:
                    pass
                else:
                    return await ctx.message.reply(f"You don't own a cookbook! Use `{ctx.prefix}pbuy cookbook` to buy one!")
            except Exception as error:
                if isinstance(error, TypeError):
                    return await ctx.message.reply("***Use `!setup` to set up your pet inventory***")
                else:
                    raise error
            with open("./plates.json") as f:
                plates = json.load(f)
            checkedplates = []
            user_ing = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['ingredients']
            if user_ing == {}:
                return await ctx.message.reply("***You don't have enough ingredients!***")
            valid = False
            found = False
            ok = True
            while not valid:
                while len(checkedplates) < 50:
                    try:
                        randomplate = random.choice(list(plates.keys()))
                        if randomplate in checkedplates:
                            continue
                        else:
                            ok = True
                            checkedplates.append(randomplate)
                            for x in plates[randomplate]['ingredients']:
                                try:
                                    ingamount = user_ing[x[0]][x[1]]
                                except:
                                    ingamount = 0
                                if ingamount - x[2] >= 0 and ok == True:
                                    continue
                                else:
                                    ok = False
                                    break
                            if ok == True:
                                valid = True
                                break
                    except:
                        pass
                if valid == True:
                    found = True
                else:
                    valid = True
            if found is False:
                return await ctx.message.reply("***You don't have enough ingredients for any dish!***")
            else:
                try:
                    discovered_recipes = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()["cookbook"]
                    try:
                        plate_recipe = discovered_recipes[randomplate]
                        embed = discord.Embed(color=discord.Color.gold(), description=f"You cooked `{randomplate}`")
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        embed.set_thumbnail(url=plates[randomplate]["image"])
                    except Exception as error:
                        if isinstance(error, KeyError):
                            embed = discord.Embed(
                                color=discord.Color.gold(),
                                title=f"You discovered a new recipe!\n\n**Value: **{plates[randomplate]['price']}",
                                description=f"`{randomplate}` has been added to your cookbook\n\n**Recipe:**",
                                timestamp=datetime.datetime.utcnow()
                            )
                            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            embed.set_thumbnail(url=plates[randomplate]["image"])
                            embed.add_field(name="Ingredient", value="\n".join(list(map(lambda ingr: ingr[1], plates[randomplate]["ingredients"]))))
                            embed.add_field(name="Quantity", value="\n".join(list(map(lambda ingr: str(ingr[2]), plates[randomplate]["ingredients"]))))
                            embed.add_field(name="Rarity", value="\n".join(list(map(lambda ingr: ingr[0], plates[randomplate]["ingredients"]))))
                except Exception as error:
                    raise error
                await ctx.send(embed=embed)
                user_ingredients = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()["ingredients"]
                for ingr in plates[randomplate]["ingredients"]:
                    if user_ingredients[ingr[0]][ingr[1]] - ingr[2] <= 0:
                        db.collection("petinventory").document(f"{ctx.author.id}").set({
                            "ingredients": {
                                    ingr[0]: {
                                    ingr[1]: firestore.DELETE_FIELD
                                }
                            }
                        }, merge=True)
                    else:
                        db.collection("petinventory").document(f"{ctx.author.id}").set({
                            "ingredients": {
                                    ingr[0]: {
                                    ingr[1]: user_ingredients[ingr[0]][ingr[1]] - ingr[2]
                                }
                            }
                        }, merge=True)
                try:
                    dish_count = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()["dishes"][randomplate]
                    db.collection("petinventory").document(f"{ctx.author.id}").set({
                        "dishes": {
                            randomplate: dish_count + 1
                        }
                    }, merge=True)
                except Exception as error:
                    if isinstance(error, KeyError):
                        db.collection("petinventory").document(f"{ctx.author.id}").set({
                            "dishes": {
                                randomplate: 1
                            }
                        }, merge=True)
                    else:
                        raise error
                db.collection("petinventory").document(f"{ctx.author.id}").set({
                        "cookbook": {
                            randomplate: True
                        }
                    }, merge=True)
        else:
            plate = plate.lower().replace(" ", "")
            try:
                plate = self.plates[plate]
            except KeyError:
                return await ctx.message.reply("***Not a valid plate!***")
            thread_pool = ThreadPoolExecutor()
            partial_sell = partial(self.cook_plate, ctx.author, plate)
            result = await self.bot.loop.run_in_executor(thread_pool, partial_sell)
            if type(result) is str:
                await ctx.message.reply(result)
            else:
                await ctx.send(embed=result)

    @commands.command(help="Sell your cooked dishes.", usage="dishsell <plate>", aliases=["selldish", "dsell", "sellplate", "platesell"], case_insensitive=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dishsell(self, ctx, *, plate: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        if plate is None:
            return await ctx.message.reply("***Specify a dish from your inventory!***")
        plate = plate.lower().replace(" ", "")
        try:
            plate = self.plates[plate]
        except KeyError:
            return await ctx.message.reply("***Not a valid plate!***")
        thread_pool = ThreadPoolExecutor()
        partial_sell = partial(self.sell_plate, ctx.author, plate)
        result = await self.bot.loop.run_in_executor(thread_pool, partial_sell)
        if type(result) is str:
            await ctx.message.reply(result)
        else:
            await ctx.send(embed=result)

    @commands.command(help="Sell all your cooked dishes.", usage="dishsellall", aliases=["selldishall", "dsellall", "sellplateall", "platesellall"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dishsellall(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        try:
            dishes = db.collection("petinventory").document(f"{ctx.author.id}").get().to_dict()["dishes"]
            if dishes == {}:
                return await ctx.message.reply("***You have no dishes to sell!***")
            with open("./plates.json") as f:
                plates = json.load(f)
            coins = 0
            for dish, amount in dishes.items():
                coins += plates[dish]["price"] * amount
            bal = db.collection("balance").document(f"{ctx.author.id}").get().to_dict()["coins"]
            db.collection("balance").document(f"{ctx.author.id}").set({
                "coins": bal + coins
            }, merge=True)
            db.collection("petinventory").document(f"{ctx.author.id}").set({
                "dishes": {}
            }, merge=True)
            embed = discord.Embed(description=f"Succesfully sold all your dishes for **{coins}**<:coin:845012771594043412>", color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                return await ctx.message.reply("***You have no dishes to sell!***")
            elif isinstance(error, TypeError):
                return await ctx.message.reply("***You have no dishes to sell!***")
            else:
                raise error

    @commands.command(help="Feed the dish to your pet!.", usage="feed {dish}")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def feed(self,ctx, *, args: typing.Optional[str]):
        # if ctx.channel.id != 728299872947667106:
        #     return
        if args is None or args == "":
            await ctx.message.add_reaction('❌')
            return
        pet = await self.getpet(ctx.author.id)
        if pet == "":
            return await ctx.send("You don't have any pet equipped")
        try:
            plate = self.plates[args.lower()]
        except Exception as error:
            if isinstance(error,KeyError):
                return await ctx.send("Could not find that plate!")
        allplates = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['dishes']
        have = False
        for x in allplates.keys():
            if plate == x:
                have = True
        if have is False:
            return await ctx.send("You do not have that plate!")
        else:
            try:
                lastfeed = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['cooldowns']['feed']
                then = lastfeed
                today = int(round(time.time()*1000))
                todaydate = datetime.datetime.fromtimestamp(today/1e3)
                thendate = datetime.datetime.fromtimestamp(43200+then/1e3)
                timeleft = abs(todaydate-thendate)
                seconds = timeleft.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                if todaydate < thendate:
                    return await ctx.message.reply(f"You can feed your pet again in **{str(hours) + 'h ' + str(minutes) + 'm ' + str(seconds) + 's'}**")
                db.collection(u"petinventory").document(f"{ctx.author.id}").set({'cooldowns':{'feed': int(round(time.time() * 1000))}},merge=True)
            except Exception as error:
                if isinstance(error,KeyError):
                    db.collection(u"petinventory").document(f"{ctx.author.id}").set({'cooldowns':{'feed': int(round(time.time() * 1000))}},merge=True)
                else:
                    raise error
            amount = allplates[self.plates[args]]
            if amount == 1:
                db.collection('petinventory').document(f'{ctx.author.id}').set({'dishes':{
                    self.plates[args.lower()]: firestore.DELETE_FIELD
                }},merge=True)
            else:
                db.collection('petinventory').document(f'{ctx.author.id}').set({'dishes':{
                    self.plates[args.lower()]: amount-1
                }},merge=True)
            try:
                lvl = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['Level']
                xp = db.collection('petinventory').document(f'{ctx.author.id}').get().to_dict()['pets'][pet]['XP']
            except Exception as error:
                if isinstance(error,KeyError):
                    lvl = 0
                    xp = "not owned"
            if type(xp) == str:
                return await ctx.send("You are at MAX LEVEL!") 
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
            if xp + 50 < xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    pet: {
                        'XP': xp + 50
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'You fed {pet} with {self.plates[args.lower()]} and it gained 50 XP!')
                embed.set_thumbnail(url=self.pet_urls[pet])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            if xp+50 >= xpcap and lvl != 5:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets':{
                    pet: {
                        'Level': lvl + 1,
                        'XP': 0
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Your pet leveled up! Current level: `{lvl+1}`')
                embed.set_thumbnail(url=self.pet_urls[pet])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            elif lvl == 5 and xp+50 >= xpcap:
                db.collection('petinventory').document(f'{ctx.author.id}').set({u'pets': {
                    pet: {
                        'XP': 'MAX LEVEL'
                    }}},merge=True)
                embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f'Level: MAX LEVEL')
                embed.set_thumbnail(url=self.pet_urls[pet])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        '''
        maybe feedall(gets all plates and feeds the pet + 50 x platenr)
        do feedall by getting the len of plates then removing all of them aight good night
        '''
        
        
def setup(bot):
    bot.add_cog(Cooking(bot))
