import discord
from discord.ext import commands

class deverify(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    def getDeverified(self, a = ""):
        dat = ""
        ret = False
        file1 = open("verified.csv", "r")

        for line in file1:
            if a not in line.split(","):
                dat += line
            else:
                ret = True

        file1.close()

        file1 = open("verified.csv", "w")
        file1.write(dat)
        file1.close()

        return ret

    #commands
    @commands.command(aliases = ['d', 'deverify'])
    async def _deverify(self, ctx, member=""):
        if member == "":
            await ctx.channel.send("mention a member as argument")
            return

        user = ""
        try:
            user = await commands.MemberConverter().convert(ctx, member)
        except:
            await ctx.channel.send("mention a valid member")
            return

        if ("Admin" in [i.name for i in ctx.author.roles]) or ("Bot Dev" in [i.name for i in ctx.author.roles]):
            if self.getDeverified(str(user.id)):
                role = discord.utils.get(ctx.guild.roles, name="Verified")
                branch = discord.utils.get(ctx.guild.roles, name=[i.name for i in user.roles][2])
                await user.remove_roles(role)
                await user.remove_roles(branch)
                await ctx.channel.send(f"deverified {user.mention}")
            else:
                await ctx.channel.send(f"{ctx.author.mention} user has not been verified")
        else:
            await ctx.channel.send("you do not have access to this command")


    
def setup(client):
    client.add_cog(deverify(client))