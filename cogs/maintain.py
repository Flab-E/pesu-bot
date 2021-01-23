import discord
from discord.ext import commands
import asyncio

class maintain(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot_logs = 749473757843947671

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


    #events
    @commands.Cog.listener()
    async def on_member_remove(self, user):
        await self.client.get_channel(self.bot_logs).send(f'{user.name}#{user.id} just left.')
        if self.getDeverified(str(user.id)):
            await user.remove_roles('Verified')
            await self.client.get_channel(self.bot_logs).channel.send(f"deverified {user.mention}")

    @commands.command(aliases = ['c', 'count'])
    async def _count(self, ctx, *roleName):
        roleName = ' '.join(roleName)
        #convert it back into string and split it at '&' and strip the individual roles
        try:
            roleName = roleName.split('&')
        except:
            pass
        temp = []
        for i in roleName:
            temp.append(i.strip())
        roleName = temp
        await ctx.send("Got request for role " + str(roleName))
        #A command to get number of users in a role
        if roleName == ['']:
            for guild in self.client.guilds:
                await ctx.send("We have {} people here, wow!!".format(len(guild.members)))
        else:
            thisRole = []
            #make a list of all roles in terms of role-id
            for roles in roleName:
                thisRole.append(discord.utils.get(ctx.guild.roles, name=roles))
            for guild in self.client.guilds:
                count = 0
                for member in guild.members:
                    boolean = True
                    #bool will be true only if all the roles passed as args are present
                    for roles in thisRole:
                        if roles not in member.roles:
                            boolean = False
                    if boolean:    
                        count += 1
            await ctx.send(str(count) + " people has role " + str(thisRole))

    @commands.command(aliases = ['p', 'purge'])
    async def _clear(self, ctx, amt=5):
        rls = [r.name for r in ctx.author.roles]
        if ("Admin" in rls) or ("Bot Dev" in rls):
            await ctx.channel.purge(limit=amt)
            # Both admin and BotDev can now purge
        else:
            await ctx.channel.send(f"{ctx.author.mention} You do not have the permissions to execute this command")
            return

    @commands.command(aliases = ["mute"])
    async def _mute(self, ctx, member, time, reason="no reason given"):

        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        mods = discord.utils.get(ctx.guild.roles, name="Moderators")
        # bb = discord.utils.get(ctx.guild.roles, name="Bot Dev")
        muted = discord.utils.get(ctx.guild.roles, name="Muted")

        if ((admin in ctx.author.roles) or (mods in ctx.author.roles)):
            if '@' in str(member):
                member = str(member)
                id = ''
                for i in member:
                    if i in '1234567890':
                        id += i
                member = int(id) #get their id
                member = ctx.message.guild.get_member(member)
                
                seconds=0
                if time.lower().endswith("d"):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                if time.lower().endswith("h"):
                    seconds += int(time[:-1]) * 60 * 60
                elif time.lower().endswith("m"):
                    seconds += int(time[:-1]) * 60
                elif time.lower().endswith("s"):
                    seconds += int(time[:-1])
                
                if seconds <= 0:
                    await ctx.channel.send(f"{ctx.author.mention}, please enter a valid amount of time")
                else:
                    if (muted in member.roles):
                        await ctx.channel.send("Lawda he's already muted means how much more you'll do")
                    else:
                        if ((admin in member.roles) or (mods in member.roles)):
                            await ctx.channel.send("Lawda, he's an admin/mod. I can't mute him")
                        else:
                            await member.add_roles(muted)
                            mute_embed = discord.Embed(title="Mute", color=0xff0000)
                            mute_user = f"{member.mention} was muted"
                            mute_embed.add_field(name="Muted user", value=mute_user)
                            await ctx.channel.send(embed=mute_embed)
                            mute_embed_logs = discord.Embed(title="Mute", color=0xff0000)
                            mute_details_logs = f"{member.mention}\t Time: {time}\n Reason: {reason}\n Moderator: {ctx.author.mention}"
                            mute_embed_logs.add_field(name="Muted user", value=mute_details_logs)
                            await self.client.get_channel(778678059879890944).send(embed=mute_embed_logs)
                            await asyncio.sleep(seconds)
                            if (muted in member.roles):
                                unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
                                unmute_user = f"{member.mention} welcome back"
                                unmute_embed.add_field(name="Unmuted user", value=unmute_user)
                                await ctx.channel.send(embed=unmute_embed)
                                unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
                                unmute_details_logs = f"{member.mention}\n Moderator: Auto"
                                unmute_embed_logs.add_field(name="Unmuted user", value=unmute_details_logs)
                                await self.client.get_channel(778678059879890944).send(embed=unmute_embed_logs)
                                await member.remove_roles(muted)
            else:
                await ctx.channel.send(f"{ctx.author.mention}, mention the user, not just the name")
        else:
            await ctx.channel.send("Lawda not for your use")



    @commands.command(aliases = ["unmute"])
    async def _unmute(self, ctx, member: discord.Member):
        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        mods = discord.utils.get(ctx.guild.roles, name="Moderators")
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        # bb = discord.utils.get(ctx.guild.roles, name="Bot Dev")
        if ((admin in ctx.author.roles) or (mods in ctx.author.roles)):
            if (muted not in member.roles):
                await ctx.channel.send("Lawda he's not muted only means")
            else:
                unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
                unmute_user = f"{member.mention} welcome back"
                unmute_embed.add_field(name="Unmuted user", value=unmute_user)
                await ctx.channel.send(embed=unmute_embed)
                unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
                unmute_details_logs = f"{member.mention}\n Moderator: {ctx.author.mention}"
                unmute_embed_logs.add_field(name="Unmuted user", value=unmute_details_logs)
                await self.client.get_channel(self.bot_logs).send(embed=unmute_embed_logs)
                await member.remove_roles(muted)
        else:
            await ctx.channel.send("Lawda not for your use")

def setup(client):
    client.add_cog(maintain(client))