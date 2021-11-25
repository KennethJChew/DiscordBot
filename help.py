import os
import random
import discord
from discord import errors
from dotenv import load_dotenv
from discord.ext import commands

"""
Help command is an empty class that requires overriding
1.send_bot_help
2.send_command_help
3.send_group_help
4.send_cog_help
"""
class myHelp(commands.HelpCommand):
    
    def get_command_signature(self, command):
        return "{prefix}{command} {signature} - {help}".format(prefix=self.clean_prefix,command=command.qualified_name,signature=command.signature,help=command.help)
    

    """
    Triggered when someone types <prefix>help


    """
    async def send_bot_help(self,mapping):
        print("!help command entered")
        embed = discord.Embed(title="Help",description="Refer below for the full list of commands that the bot supports.\nType {prefix}help <command>for detailed explanations on each individual command.".format(prefix=self.clean_prefix))
        for cog,commands in mapping.items():
            
            if cog:
                print("Cog exists, getting cog commands...")
                print("Cog:{0},Commands:{1}".format(cog.qualified_name,len(commands)))
                cog_commands = cog.get_commands()
                print("There are {0} commands.".format(len(commands)))
                print("Commands are:")
                command_count = 0
                for command in cog_commands:
                    command_count += 1
                    print(str(command))
                print("Filtering cog commands...")
                filtered_commands = await self.filter_commands(commands,sort=True)
                print("Filtered commands:")
                print(filtered_commands)
                command_count = 0
            else:
                print("There is no cog,filtering native bot commands...")
                print("There are {0} native bot commands".format(len(commands)))
                print("Commands are:")
                command_count = 0
                for command in commands:
                    command_count += 1
                    print(str(command) + command.name)
                print("Filtering cog commands...")
                filtered_commands = await self.filter_commands(commands,sort=True)
                print("Filtered commands:")
                print(filtered_commands)
                command_count = 0

            print("printing cog signatures")
            command_signatures = [self.get_command_signature(c) for c in filtered_commands]
            print(command_signatures)

            if command_signatures:
                # Get the attribute named "qualified name" from the cog. If there is none, default is No Category
                print("Command sig exists")
                cog_name = getattr(cog,"qualified_name","Commands")
                print("Cog name is " + cog_name)
                embed.add_field(name=cog_name,value="\n".join(command_signatures),inline=False)
                
            else:
                print("Command sig does not exist")
                # raise errors.DiscordException("No command signatures found")
        output_channel = self.get_destination()
        await output_channel.send(embed=embed)





    #!help <command>
    """
    Triggered when someone types >prefix>help <command>

    Sends a message containing the description "help" description of the command and the parameters of the command(if any) with examples
    """
    async def send_command_help(self,command):
        # Set headers and subheader
        embed_title = "Details for the command " + command.qualified_name
        embed = discord.Embed(title=embed_title,description="An explanation so simple even YOU can understand!")
        # Add the command's help description
        embed.add_field(name="What it does",value=command.help,inline=False)
        # How to use it
        cmd_signature = command.signature
        if cmd_signature:
            embed.add_field(name="What additional fields does it take",value=cmd_signature,inline=False)
        else:
            embed.add_field(name="What additional fields does it take",value="This command does not have any additional fields that you need to enter",inline=False)
        # Add detail on how to use it
        args = command.signature.split(" ")
        print(args)
        cmd_tutorial="{prefix}{command} {arg}".format(prefix=self.clean_prefix,command=command.qualified_name,arg=" ".join([arg for arg in args]))
        embed.add_field(name="How to use it",value=cmd_tutorial)

        output_channel = self.get_destination()
        await output_channel.send(embed=embed)
    #!help <group>
    async def send_group_help(self,group):
        await self.context.send("This is the help group")
    #!help <cog>
    async def send_cog_help(self,cog):
        await self.context.send("This is the help cog")
    # Called when !help <command> is entered and <command> is not found
    def command_not_found(self, string):
        print('dsadas')
        return super().command_not_found(string)

    async def on_help_command_error(self, ctx, error):
        print("On help commadn error")
        if isinstance(error,commands.BadArgument):
            embed = discord.Embed(title="Error",description=str(error))
            await ctx.send(embed=embed)
        else:
            print(error)
    # called after the function command_not_found is called
    async def send_error_message(self, error):
        print("Send error msg invoked")
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

# class myCog(commands.Cog):
#     def __init__(self,bot):
#         self.original_help_command = bot.help_command
#         bot.help_command = myHelp()
#         bot.help_command.cog = self

#     def cog_unload(self):
#         self.bot.help_command = self.original_help_command
