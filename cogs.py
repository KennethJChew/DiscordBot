from logging import raiseExceptions
import discord
from discord import errors
from discord.ext import commands
from help import myHelp

class Greetings(commands.Cog):
    """
    Collection of commands that are to be called when new user joins the discord server
    """
    def __init__(self,bot) -> None:
        self.bot = bot
        self._last_member = None
        help_command = myHelp()
        help_command.cog = self
        bot.help_command = help_command

    @commands.Cog.listener()
    async def on_member_join(self,member):
        """
        
        """
        print("On member join called")
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Welcome {user.mention} to {server}.".format(user=member,server=member.guild))
        else:
            raise errors.DiscordException("Error in {0}".format(self.qualified_name))
            
    
    @commands.command()
    async def hello(self,ctx,*,member:discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member != member.id:
            await ctx.send("Hello {0.name}~~~~".format(member))
        else:
            await ctx.send("Hello {0.name}.... You seem familiar...".format(member))
        self._last_member = member

    async def cog_check(self, ctx):

        print("COG CHECK")
        roles_list = ctx.author.roles
        print("List length:" + str(len(roles_list)))
        for role in roles_list:
            if "admin" in role.name:
                print("PASS")
                print(role)
                return True
            else:
                print("FALSE")
                print(role)
        return False


    

