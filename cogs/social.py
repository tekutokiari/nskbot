import discord
from discord.ext import commands
from firebase_admin import firestore
import datetime
from dpymenus import Page, PaginatedMenu
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import typing
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from functools import partial
from discord import File
import textwrap
import time
import firebase_admin

db = firestore.client(firebase_admin._apps['maindb'])

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Social"

    def getpet(self,user):
        try:
            pet = db.collection('petinventory').document(f'{user}').get().to_dict()['pet']
            return pet
        except:
            pass
    @staticmethod
    def coin_leaderboard(ctx, function_index: int = 0):
        i = 1
        top_rupee = ""
        ids = []
        rupeelb = db.collection('balance').order_by("coins", direction=firestore.Query.DESCENDING).limit(10).stream()
        for doc in rupeelb:
            ids.append(doc.id)
            if db.collection(u'uno').document(f"{doc.id}").get().to_dict()['activated'] == 'true':
                top_rupee += f"**{i}.** <:uno_reverse_card:913440883653877840> " + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ " + str(doc.to_dict()['coins']) + "<:coin:845012771594043412>" + "\n"
                i += 1
            else:
                top_rupee += f"**{i}.**" + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ " + str(doc.to_dict()['coins']) + "<:coin:845012771594043412>" + "\n"
                i += 1
        return (top_rupee, function_index)

    @staticmethod
    def shiny_leaderboard(ctx, function_index: int = 1):
        i = 1
        top_shiny = ""
        ids = []
        shinylb = db.collection(u'shiny').order_by("shiny", direction=firestore.Query.DESCENDING).limit(10).stream()
        for doc in shinylb:
            ids.append(doc.id)
            top_shiny += f"**{i}.** " + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ " + str(doc.to_dict()['shiny']) + "<:1_shiny_rupee:755974674927845456>" + "\n"
            i += 1
        return (top_shiny, function_index)

    @staticmethod
    def splash_leaderboard(ctx, function_index: int = 2):
        i = 1
        top_splash = ""
        ids = []
        splashes = db.collection(u'splash').order_by("splashes", direction=firestore.Query.DESCENDING).limit(10).stream()
        for doc in splashes:
            ids.append(doc.id)
            top_splash += f"**{i}.** " + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ " + str(doc.to_dict()['splashes']) + " splashes" + "\n"
            i += 1
        return (top_splash, function_index)

    @staticmethod
    def eep_leaderboard(ctx, function_index: int = 3):
        i = 1
        top_eep = ""
        ids = []
        eeps = db.collection(u'eep').order_by("eep", direction=firestore.Query.DESCENDING).limit(10).stream()
        for doc in eeps:
            ids.append(doc.id)
            top_eep += f"**{i}.** " + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ " + str(doc.to_dict()['eep']) + " <:cheep_eep:752019232643874827>" + "\n"
            i += 1
        return (top_eep, function_index)

    @staticmethod
    def streak_leaderboard(ctx, function_index: int = 4):
        i = 1
        top_streak = ""
        ids = []
        streaks = db.collection(u'streak').order_by("streak", direction=firestore.Query.DESCENDING).limit(10).stream()
        for doc in streaks:
            ids.append(doc.id)
            top_streak += f"**{i}.** " + str(discord.utils.get(ctx.guild.members, id=int(ids[i-1]))) + " ─ Streak: " + str(doc.to_dict()['streak']) + "\n"
            i += 1
        return (top_streak, function_index)

    @commands.command(help="See the bot's leaderboards.", usage="leaderboard <category>", aliases=['lb', 'leaderboard'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leaderboards(self, ctx):
        if ctx.channel.id != 728299872947667106:
            return
        message = await ctx.send("**Generating Leaderboards! (this might take a bit)...**")
        rupeepage = Page(title="Rupee Leaderboard", color=discord.Color.gold())
        shinypage = Page(title="Shiny Rupee Leaderboard", color=discord.Color.gold())
        eeppage = Page(title="Eep Cheep Leaderboard", color = discord.Color.gold())
        streakpage = Page(title="Streak Leaderboard", color = discord.Color.gold())

        futures = []
        result_list = []

        with ThreadPoolExecutor() as thread_pool:
            futures.append(thread_pool.submit(self.coin_leaderboard, ctx))
            futures.append(thread_pool.submit(self.shiny_leaderboard, ctx))
            futures.append(thread_pool.submit(self.eep_leaderboard, ctx))
            futures.append(thread_pool.submit(self.streak_leaderboard, ctx))
            for future in concurrent.futures.as_completed(futures):
                result_list.append(future.result())

        for result in result_list:
            if result[1] == 0:
                rupeepage.add_field(name="Users: ", value=result[0], inline=False)
                rupeepage.set_author(name="NS Kingdom", icon_url=self.bot.user.avatar_url)
            elif result[1] == 1:
                shinypage.add_field(name="Users: ", value=result[0], inline=False)
                shinypage.set_author(name="NS Kingdom", icon_url=self.bot.user.avatar_url)
            elif result[1] == 3:
                eeppage.add_field(name="Users: ", value=result[0], inline=False)
                eeppage.set_author(name="NS Kingdom", icon_url=self.bot.user.avatar_url)
            elif result[1] == 4:
                streakpage.add_field(name="Users: ", value=result[0], inline=False)
                streakpage.set_author(name="NS Kingdom", icon_url=self.bot.user.avatar_url)
        menu = PaginatedMenu(ctx)
        menu.add_pages([rupeepage, shinypage, eeppage, streakpage])
        await message.edit(content="Done!", delete_after=1.2)
        await menu.open()

    @commands.command(help="Search for someone that wants to play with you.", usage="findp <game>(optional)", aliases=['fp'])
    async def findp(self,ctx,*,args:typing.Optional[str]):
        ids = [727957656483921931,727957726231134313,727957922029633596,759448232412577792]
        if ctx.channel.id not in ids:
            return
        try:
            lastfindp = db.collection('findp').document(f'{ctx.author.id}').get().to_dict()['cooldown']
            then = lastfindp
            today = int(round(time.time()*1000))
            todaydate = datetime.datetime.fromtimestamp(today/1e3)
            thendate = datetime.datetime.fromtimestamp(300+then/1e3)
            timeleft = abs(todaydate-thendate)
            seconds = timeleft.seconds
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if todaydate < thendate:
                return await ctx.message.reply(f"You can ping to play again in **{str(minutes) + 'm ' + str(seconds) + 's'}**")
            db.collection(u"findp").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
        except Exception as error:
            if isinstance(error,TypeError):
                db.collection(u"findp").document(f"{ctx.author.id}").set({u'cooldown': int(round(time.time() * 1000))},merge=True)
            else:
                raise error
        if not args or args is None:
            return await ctx.send(f"<@&733372303676801126> \n **> {ctx.author.name}** wants to play! \n Anyone down?")
        else:
            return await ctx.send(f"<@&733372303676801126> \n **> {ctx.author.name}** wants to play **{args}**! \n Anyone down?")

    @commands.group(
        help="Switch friend code related commands. Set/delete your friend code or retrieve someone's friend code.",
        usage="friendcode <option>", aliases=["fc"], case_insensitivie=True
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def friendcode(self, ctx):
        channels = [759448232412577792, 864382698243358741, 727957726231134313, 727957656483921931, 728299872947667106, 728299872947667106]
        if ctx.channel.id not in channels: 
            return
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Color.gold(), description=f"Switch Friend Code related commands.\n*ex: {ctx.prefix}friendcode <option>*")
            embed.set_author(name="NS Kingdom", icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Available Categories", value="*set, delete, get*")
            await ctx.send(embed=embed)

    @friendcode.command(help="Set your Switch Friend Code.", usage="friendcode set <code>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def set(self, ctx, code = None):
        channels = [759448232412577792, 864382698243358741, 727957726231134313, 727957656483921931, 728299872947667106, 728299872947667106]
        if ctx.channel.id not in channels: 
            return
        if code is None:
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value="```No code specified!```")
            return await ctx.send(embed=embed)
        db.collection("switch").document(f"{ctx.author.id}").set({
            "userName": ctx.author.name,
            "userID": ctx.author.id,
            "sfc": code
        }, merge=True)
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f"Changed your Switch Friend Code to ***{code}***")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @friendcode.command(help="Delete your Switch Friend Code.", usage="friendcode delete")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx):
        channels = [759448232412577792, 864382698243358741, 727957726231134313, 727957656483921931, 728299872947667106, 728299872947667106]
        if ctx.channel.id not in channels: 
            return
        db.collection("switch").document(f"{ctx.author.id}").set({
            "sfc": firestore.DELETE_FIELD
        }, merge=True)
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description="Deleted your Switch Friend Code")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @friendcode.command(help="Get your or someone else's Switch Friend Code.", usage="friendcode get @user(optional - defaults to command invoker)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def get(self, ctx, user: discord.User = None):
        channels = [759448232412577792, 864382698243358741, 727957726231134313, 727957656483921931, 728299872947667106, 728299872947667106]
        if ctx.channel.id not in channels: 
            return
        if user is None:
            user = ctx.author
        try:
            code = db.collection("switch").document(f"{user.id}").get().to_dict()["sfc"]
            code = f"Switch Friend Code: ***{code}***"
        except Exception as error:
            if isinstance(error, KeyError):
                code = "No Switch Friend Code set."
            elif isinstance(error, TypeError):
                code = "No Switch Friend Code set."
            else:
                raise error
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=code)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Set your profile card background.", usage="bgset `number` (0 for default background)", aliases=["backgroundset", "setbg", "setbackground"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bgset(self, ctx, number: int = None):
        if ctx.channel.id != 728299872947667106:
            return
        if number is None:
            embed = discord.Embed(title="Incorect use of `bgset` command!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            embed.add_field(name="Correct use", value=f"```{ctx.prefix}bgset <number>```")
            return await ctx.message.reply(embed=embed)
        elif number not in range(0, 57):
            embed = discord.Embed(title="Incorect use of `bgset` command!", timestamp=datetime.datetime.utcnow(), color=discord.Color.gold())
            embed.add_field(name="Error", value="```Background not found!```")
            return await ctx.message.reply(embed=embed)
        try:
            owned_bgs = db.collection("profile").document(f"{ctx.author.id}").get().to_dict()["ownedbgs"]
            if number not in owned_bgs:
                return await ctx.message.reply("***You don't own this background.***")
            db.collection("profile").document(f"{ctx.author.id}").set({
                "ownedbgs": owned_bgs,
                "bgset": number
            }, merge=True)
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection("profile").document(f"{ctx.author.id}").set({
                    "ownedbgs": [0],
                    "bgset": 0
                }, merge=True)
                return await ctx.message.reply("***You don't own this background.***")
            else:
                raise error
        embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow(), description=f"Succesfully changed profile background to `{number}`")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Set your profile description.", usage="setabout <text>", aliases=["setdescription", "setdescr", "description"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def setabout(self, ctx, *, text: str = None):
        if ctx.channel.id != 728299872947667106:
            return
        if text is None:
            return await ctx.message.reply("You can set nothing as a description only literally.")
        elif len(text) > 425:
            return await ctx.message.reply("Description too long.")
        db.collection("profile").document(f"{ctx.author.id}").set({
            "description": text
        }, merge=True)
        embed = discord.Embed(color=discord.Color.gold(), description="Succesfully set profile description.")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @staticmethod
    def get_avatar(buffer: BytesIO, resize: tuple, rad: int, function_index: int = 0):
        buffer.seek(0)
        avatar_image = Image.open(buffer)
        avatar_image = avatar_image.resize(resize)
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', avatar_image.size, 255)
        w, h = avatar_image.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        avatar_image.putalpha(alpha)
        return (avatar_image, function_index)

    @staticmethod
    def get_background(user_id: int, rad: int, function_index: int = 1):
        try:
            bg_set = db.collection("profile").document(f"{user_id}").get().to_dict()["bgset"]
        except Exception as error:
            if isinstance(error, TypeError):
                db.collection("profile").document(f"{user_id}").set({
                    "ownedbgs": [0],
                    "bgset": 0
                }, merge=True)
                bg_set = 0
            else:
                raise error
        if bg_set == 0:
            background = Image.open(f"./images/{bg_set}.jpg")
        else:
            background = Image.open(f"./profile backgrounds/{bg_set}.jpg")
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', background.size, 255)
        w, h = background.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        background.putalpha(alpha)
        return (background, function_index)

    @staticmethod
    def get_badges(member: discord.Member, function_index: int = 2):
        badges_bg = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))
        roles = {
            728432964161241187: "hammer-badge.png",
            727634503962591345: "battery-badge.png",
            737186357834809374: "money-badge.png",
            735576193990000741: "stars-badge.png",
            732765784333615165: "star-badge.png",
            735187995787001957: "scroll-badge.png",
            728710674166841476: "cd-badge.png",
            742379201252032552: "mailbox-badge.png",
            751890890166894632: "fish-badge.png",
            730294598844547164: "passport-badge.png"
        }
        roles_test = {
            833119201371226162: "hammer-badge.png",
            833120698456866836: "battery-badge.png",
            833120892779102268: "money-badge.png",
            833127117092814898: "stars-badge.png",
            833128418845392926: "star-badge.png",
            833308095710887957: "scroll-badge.png",
            838905788276801566: "cd-badge.png",
            838905871492579389: "mailbox-badge.png",
            838905938710757418: "fish-badge.png",
            838905940014792706: "passport-badge.png"
        }
        x, y, badge_count = 1135, 15, 0
        for role in member.roles:
            try:
                if badge_count > 4:
                    y += 170
                    badge_count = -1
                    x = 1135
                badge = Image.open(f"./images/{roles[role.id]}").copy().convert('RGBA')
                badge = badge.resize((170, 170)).convert('RGBA')
                badges_bg.paste(badge, (x, y), badge)
                x += 150
                badge_count += 1
            except KeyError:
                pass
        staff_ids = [
            450883984600072193,  # striker
            396002772568506369,  # rocky
            310951460034707457,  # slimey
            465138950223167499,  # robert
            449555448010375201,  # teku
            393888245097693205,  # queen k rool
            494982490713358356,  # star
            724886694704185355,  # peter
            381536467597656064,  # j13
            441725592795086850,  # kleeb
            520714237895639040,  # bucket
            768492917773828126,  # wiseburger
            454335298898231310  # jakob
        ]
        if member.id in staff_ids or badge_count >= 9:
            staff_star = Image.open('./images/staff-stars.png').convert('RGBA')
            staff_star = staff_star.resize((100, 100))
            badges_bg.paste(staff_star, (1805, 970), staff_star)
        return (badges_bg, function_index)

    def get_text(self, member: discord.Member, function_index: int = 3):
        text_bg = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))
        rectangle1 = Image.open("./images/round-rectangle1.png").convert('RGBA')
        rectangle1 = rectangle1.resize((770, 265))
        rectangle2 = Image.open("./images/round-rectangle2.png").convert('RGBA')
        rectangle2 = rectangle2.resize((1764, 455))
        rupee = Image.open("./images/rupee.png").convert('RGBA').convert('RGBA')
        rupee = rupee.resize((55, 55))
        shiny_rupee = Image.open("./images/shiny.png").convert('RGBA')
        shiny_rupee = shiny_rupee.resize((70, 70))
        eep = Image.open("./images/eep.png").convert('RGBA')
        eep = eep.resize((70, 70))
        text_bg.paste(rectangle1, (350, 45), rectangle1)
        text_bg.paste(rectangle2, (30, 600), rectangle2)
        text_bg.paste(rupee, (50, 635), rupee)
        text_bg.paste(shiny_rupee, (45, 700), shiny_rupee)
        text_bg.paste(eep, (50, 775), eep)

        try:
            coins = db.collection("balance").document(f"{member.id}").get().to_dict()["coins"]
        except Exception as error:
            if isinstance(error, TypeError):
                coins = 0
            elif isinstance(error, KeyError):
                coins = 0
            else:
                raise error
        try:
            shiny = db.collection("shiny").document(f"{member.id}").get().to_dict()["shiny"]
        except Exception as error:
            if isinstance(error, TypeError):
                shiny = 0
            elif isinstance(error, KeyError):
                shiny = 0
            else:
                raise error
        try:
            friend_code = db.collection("switch").document(f"{member.id}").get().to_dict()["sfc"]
        except Exception as error:
            if isinstance(error, TypeError):
                friend_code = "Not set."
            elif isinstance(error, KeyError):
                friend_code = "Not set."
            else:
                raise error
        try:
            eeps = db.collection("eep").document(f"{member.id}").get().to_dict()["eep"]
        except Exception as error:
            if isinstance(error, TypeError):
                eeps = 0
            elif isinstance(error, KeyError):
                eeps = 0
            else:
                raise error
        try:
            streak = db.collection("streak").document(f"{member.id}").get().to_dict()["streak"]
        except Exception as error:
            if isinstance(error, TypeError):
                streak = 0
            elif isinstance(error, KeyError):
                streak = 0
            else:
                raise error
        try:
            about = db.collection("profile").document(f"{member.id}").get().to_dict()["description"]
        except Exception as error:
            if isinstance(error, TypeError):
                about = "No description set."
            elif isinstance(error, KeyError):
                about = "No description set."
            else:
                raise error
        about = textwrap.wrap(about, width=40)
        about = "\n".join(about)

        with open("./fonts/LBRITE.TTF", "rb") as f:
            bytes_ = BytesIO(f.read())
            font = ImageFont.truetype(bytes_, 40)
        draw = ImageDraw.Draw(text_bg)

        draw.text((370, 110), f"Name: {member}", fill="#ff0000", font=font)
        draw.text((370, 180), f"SFC: {friend_code}", fill="#eeff00", font=font)
        draw.text((110, 640), f"Coins: {coins}", fill="#e5c435", font=font)
        draw.text((110, 710), f"Shiny Rupees: {shiny}", fill="#1b7079", font=font)
        draw.text((130, 790), f"Cheep Eeps: {eeps}", fill="#d68900", font=font)
        draw.text((120, 870), f"Daily Streak: {streak}", fill="#fffffe", font=font)
        draw.text((750, 640), f"{about}", fill="#fffffe", font=font)

        return (text_bg, function_index)

    @staticmethod
    def get_pet(user_id: int, function_index: int = 4):
        pet_bg = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))
        with open("./fonts/LBRITE.TTF", "rb") as f:
            bytes_ = BytesIO(f.read())
            font = ImageFont.truetype(bytes_, 40)
        draw = ImageDraw.Draw(pet_bg)
        try:
            pet_equipped = db.collection('petinventory').document(f'{user_id}').get().to_dict()['pet']
            pet_images = {
                "Snom": ("./pets/Snom.png", "Common"),
                "Poochy": ("./pets/Poochy.png", "Common"),
                "Thwimp": ("./pets/Thwimp.png", "Common"),
                "Polari": ("./pets/Polari.png", "Common"),
                "Bandana Dee": ("./pets/Bandana_Dee.png", "Common"),
                "Baby Yoshi": ("./pets/Baby_Yoshi.png", "Rare"),
                "Plessie": ("./pets/Plessie.png", "Rare"),
                "Korok": ("./pets/Korok.png", "Rare"),
                "Boo Guy": ("./pets/Boo_Guy.png", "Rare"),
                "K. K. Slider": ("./pets/K._K._Slider.png", "Rare"),
                "Terrako": ("./pets/Terrako.png", "Legendary"),
                "Polterpup": ("./pets/Polterpup.png", "Legendary"),
                "Judd": ("./pets/Judd.png", "Legendary"),
                "Bobby": ("./pets/Bobby.png", "Legendary"),
                "Mew": ("./pets/Mew.png", "Legendary")
            }
            colors = {
                "Common": "#ff0000",
                "Rare": "#277ecd",
                "Legendary": "#f8ff00"
            }
            pet_image = Image.open(pet_images[pet_equipped][0])
            pet_image = pet_image.convert('RGBA')
            pet_image = pet_image.resize((60, 60))
            pet_bg.paste(pet_image, (50, 950), pet_image)
            draw.text((120, 950), f"Pet equipped: {pet_equipped}", fill=colors[pet_images[pet_equipped][1]], font=font)
        except Exception as error:
            if isinstance(error, KeyError):
                pet_equipped = "No pet equipped."
                draw.text((120, 950), f"Pet equipped: {pet_equipped}", fill="#fffffe", font=font)
            elif isinstance(error, TypeError):
                pet_equipped = "No pet equipped."
                draw.text((120, 950), f"Pet equipped: {pet_equipped}", fill="#fffffe", font=font)
            else:
                raise error
        fire = Image.open("./pets/fire.png").convert('RGBA').resize((60, 60))
        pet_bg.paste(fire, (50, 860), fire)
        return (pet_bg, function_index)

    @staticmethod
    def profile_card(background: Image, avatar: Image, badges: Image, text: Image, pet: Image):
        background.convert('RGBA')
        avatar.convert('RGBA')
        badges.convert('RGBA')
        pet.convert('RGBA')

        try:
            background.paste(avatar, (30, 30), avatar)
        except Exception as error:
            if isinstance(error, ValueError):
                background.paste(avatar, (30, 30))
            else:
                raise error
        background.paste(badges, (0, 0), badges)
        background.paste(text, (0, 0), text)
        background.paste(pet, (0, 0), pet)

        output_buffer = BytesIO()
        background.save(output_buffer, format='png')
        output_buffer.seek(0)

        return output_buffer

    @commands.command(help="Display your NS Kingodm profile card.", usage="profile @user (optional)", aliases=["pf"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member = None):
        if ctx.channel.id != 728299872947667106:
            return
        async with ctx.channel.typing():
            if member is None:
                member = ctx.author

            avatar_buffer = BytesIO()
            member_avatar = member.avatar_url_as(format='png', size=256)
            await member_avatar.save(avatar_buffer)

            futures = []
            result_list = []

            with ThreadPoolExecutor() as thread_pool:
                futures.append(thread_pool.submit(self.get_avatar, avatar_buffer, (300, 300), 50))
                futures.append(thread_pool.submit(self.get_background, member.id, 50))
                futures.append(thread_pool.submit(self.get_badges, member))
                futures.append(thread_pool.submit(self.get_text, member))
                futures.append(thread_pool.submit(self.get_pet, member.id))
                for future in concurrent.futures.as_completed(futures):
                    result_list.append(future.result())

            for result in result_list:
                if result[1] == 0:
                    avatar = result[0]
                elif result[1] == 1:
                    background = result[0]
                elif result[1] == 2:
                    badges = result[0]
                elif result[1] == 3:
                    text = result[0]
                elif result[1] == 4:
                    pet = result[0]

            with ThreadPoolExecutor() as thread_pool:
                profile_partial = partial(self.profile_card, background, avatar, badges, text, pet)
                profile_card = await self.bot.loop.run_in_executor(thread_pool, profile_partial)

            _file = File(profile_card, filename="profilecard.png")
            embed = discord.Embed(color=discord.Color.gold(), timestamp=datetime.datetime.utcnow())
            embed.set_author(icon_url=ctx.guild.icon_url, name="NS Kingdom")
            embed.set_image(url="attachment://profilecard.png")
            await ctx.send(file=_file, embed=embed)
            #await ctx.send(file=File(profile_card, filename="profilecard.png"))

def setup(bot):
    bot.add_cog(Social(bot))
