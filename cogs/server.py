import discord
from discord.ext import commands

class server(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot_logs = 749473757843947671

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.get_channel(self.bot_logs).send("Bot is online")
        await self.client.get_channel(self.bot_logs).send(f"Logged in as {self.client.user}")
        # On coming online, it will just text to bot_test

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #error handling, in case of an error the error message will be put up in the channel
        await self.client.get_channel(self.bot_logs).send('**Command Error**:')
        await self.client.get_channel(self.bot_logs).send(error)
        await self.client.get_channel(self.bot_logs).send('@here')


    @commands.command(aliases = ["h", "help"])
    async def _help(self, ctx):
        help_e = discord.Embed(title="PESU BOT", color=0x48bf91)
        veri = "`.v` or `.verify`\n.v help\n.v {SRN}"
        # info = "`.i` or `.info`\n.i @member"
        help_e.add_field(name="verification", value=veri)
        # help_e.add_field(name="Information", value=info)
        #New comers will never know this
        await ctx.channel.send(embed = help_e)

    #commands
    @commands.command(aliases=["e", "echo"])
    async def _echo(self, ctx, *message):
        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        mods = discord.utils.get(ctx.guild.roles, name="Moderators")
        bb = discord.utils.get(ctx.guild.roles, name="Bot Dev")

        if (
            (admin in ctx.author.roles)
            or (mods in ctx.author.roles)
            or (bb in ctx.author.roles)
        ):

            try:
                message = list(message)
                channel = message[0]
                message = message[1:]
            except Exception as E:
                await ctx.send("Lawda I'm getting this: " + str(E))
            channel = str(channel)
            newChannel = ""
            for i in channel:
                if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    newChannel += i
            message = " ".join(message)
            newChannel = int(newChannel)
            if newChannel == ctx.channel.id:
                await ctx.channel.purge(limit=1)
            await self.client.get_channel(newChannel).send(message)
        else:
            await ctx.channel.send("Sucka you can't do that")
    
def setup(client):
    client.add_cog(server(client))