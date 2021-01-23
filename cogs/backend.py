import discord
from discord.ext import commands

class backend(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.user_info = ["Member", "MemberId","PRN", "SRN", "Semester", "Section", "Hostelite", "Stream/Campus", "Stream", "Campus", "verified"]

    def getverified(self, a=""):
        if a == "": return ["unverified"]
        file = open("verified.csv", "r")

        for line in file:
            line = line.split(",")
            if len(line)>5:
                if a == line[1]:
                    file.close()
                    return line
        file.close()
        return ["unverified"]

    #commands
    @commands.command(aliases = ["info", "i"])
    async def _info(self, ctx, member):
        in_e = discord.Embed(title = "User Info", color = 0x48bf91)
        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        # mods = discord.utils.get(ctx.guild.roles, name="Moderators")
        bb = discord.utils.get(ctx.guild.roles, name="Bot Dev")
        if (admin in ctx.author.roles) or (bb in ctx.author.roles):
            try:
                user = await commands.MemberConverter().convert(ctx, member)
                data = self.getverified(str(user.id))
                if "unverified" in data:
                    await ctx.channel.send(f"{ctx.author.mention} The user has not been verified yet")
                    return

                for i in range(len(self.user_info)):
                    in_e.add_field(name=self.user_info[i], value=data[i])
                await ctx.channel.send(embed=in_e)

            except:
                await ctx.channel.send(f"{ctx.author.mention} enter a valid member")
        else:
            await ctx.channel.send("You are not authorised to do that")

    @commands.command(aliases = ["f", "file"])
    async def _file(self, ctx):
        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        # mods = discord.utils.get(ctx.guild.roles, name="Moderators")
        bb = discord.utils.get(ctx.guild.roles, name="Bot Dev")
        if (admin in ctx.author.roles) or (bb in ctx.author.roles):
            await ctx.channel.send("You have the necesarry role")
            with open("verified.csv", "r") as fp:
                await ctx.channel.send(file=discord.File(fp, 'verified.csv'))
            fp.close()
        else:
            await ctx.channel.send("You are not authorised to do that")




def setup(client):
    client.add_cog(backend(client))