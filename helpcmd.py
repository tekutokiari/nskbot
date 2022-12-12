import discord
import datetime
import random
from discord.ext import commands

class Help(commands.HelpCommand):

    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="NSK Bot Help",
            description=f"Use `{self.clean_prefix}help [command]` for details",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        for cog, cmds in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in cmds]
            if command_signatures:
                cog_name = getattr(cog, "alias", "No Category")
                if str(cog_name) != 'No Category':
                    embed.add_field(name=str(cog_name), value=f"`{self.clean_prefix}help {str(cog.qualified_name).lower()}`")
                else:
                    pass
        channel = self.get_destination()
        if channel.id != 728299872947667106:
            return
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        embed.add_field(name="Description", value=command.help)
        embed.add_field(name="Usage", value=f"{self.clean_prefix}{command.usage}", inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        else:
            embed.add_field(name="Aliases", value="`None`", inline=False)
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f"Requested by {self.context.author}")
        channel = self.get_destination()
        if channel.id != 728299872947667106:
            return
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        embed.add_field(name="Description", value=group.help)
        embed.add_field(name="Usage", value=f"{self.clean_prefix}{group.usage}", inline=False)
        alias = group.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        else:
            embed.add_field(name="Aliases", value="`None`", inline=False)
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f"Requested by {self.context.author}")
        channel = self.get_destination()
        if channel.id != 728299872947667106:
            return
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        commands = cog.get_commands()
        channel = self.get_destination()
        embed = discord.Embed(title=f"{getattr(cog, 'alias', 'No Category')}", color=random.randint(0, 0xffffff))
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f"Requested by {self.context.author}")
        embed.description = f"{', '.join(list(map(lambda x: f'`{x.qualified_name}`', commands)))}"
        if channel.id != 728299872947667106:
            return
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(color=0xbf1932, description=':exclamation: Command not found')
        channel = self.get_destination()
        if channel.id != 728299872947667106:
            return
        await channel.send(embed=embed)

attributes = {
    "cooldown": commands.Cooldown(1, 1, commands.BucketType.user),
}

help_object = Help(command_attrs=attributes)