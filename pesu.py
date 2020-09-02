import discord
from discord.ext import commands
import requests
import re

def getuser(a=""):
    if a == "": return ["error"]
    f = open("verified.csv", "r")
    srn_list = [line.split(",")[3] for line in list(filter(None, f.read().split("\n")))]
    if a in srn_list:
        f.close()
        return ["Done"]
    f.close()

    file = open("batch_list.csv", "r")

    for lin in file:
        if a in lin:
            f.close()
            return lin.split(",")

    file.close()
    return ["error"]

def getverified(a=""):
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

token = "<bot token>"
client = commands.Bot(command_prefix = ".", help_command=None)
data_list = ["PRN", "SRN", "Semester", "Section", "Hostelite", "Stream/Campus", "Stream", "Campus"]

@client.command(aliases = ["h", "help"])
async def _help(ctx):
    help_e = discord.Embed(title="PESU BOT", color=0x48bf91)
    veri = "`.v` or `.verify`\n.v help\n.v {SRN}"
    info = "`.i` or `.info`\n.i @member"
    help_e.add_field(name="verification", value=veri)
    help_e.add_field(name="Information", value=info)
    await ctx.channel.send(embed = help_e)

@client.event
async def on_ready():
    print("bot is online")
    print(f"Logged in as {client.user}")

@client.command(aliases = ['v', 'verify'])
async def _verify(ctx, SRN):
    #embed variables
    success = discord.Embed(title = "Success", color = 0x00ff00)
    fail = discord.Embed(title = "Fail", color = 0xff0000)
    veri = discord.Embed(title="Verification", description="SRN & PRN Verification process",color = 0x0000ff)
    veri.add_field(name="Process", value="1. Enter SRN (1UG19) as argument\n2. Enter PRN as text when promted by bot")
    user = ctx.author

    #help for verification:
    if "help" in SRN:
        await ctx.channel.send(embed=veri)
        return

    #checking if user entered PSN and not SRN
    if ("PES120190" in SRN) or ("PES220190" in SRN):
        veri.add_field(name="No SRN found", value="Enter SRN and not PRN as argument")
        await ctx.channel.send(f"{user.mention}", embed= veri)
        return
    
    #getting creds from pesu academy
    dat = getuser(SRN)

    if "Done" in dat:
        await ctx.channel.send(f"{user.mention} you have already been verified")
        return

    #checking if the value returned from pesu academy is an error
    if "error" in dat:
        fail.add_field(name = "Invalid SRN", value=f"SRN ({SRN}) not found")
        await ctx.send(f"{user.mention}", embed=fail)
        return
    else:
        #if valid creds are returned from pesu academy
        await ctx.channel.send(f"{user.mention} now enter PRN to complete verification")
        msg = await client.wait_for('message', check = lambda msg: msg.author == ctx.author)
        if msg.content != dat[0]:
            fail.add_field(name="PRN validation failed", value=f"PRN ({msg.content}) entered did not match the corresponding SRN ({SRN})")
            await ctx.channel.send(f"{user.mention}", embed=fail)
            return
    
        role_str = dat[-3].replace("Campus", "").replace(" ","").replace("BIOTECHNOLOGY", "BT")
        if role_str not in [r.name for r in ctx.guild.roles]:
            for each_role in ctx.guild.roles:
                if each_role.name == "Admin":
                    admin = each_role
            await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM or tag {admin.mention}")
            return
        else:
            role = discord.utils.get(user.guild.roles, name=role_str)
            await user.add_roles(role)

        for i in range(8):
            success.add_field(name="{0}".format(data_list[i]), value = dat[i])
        await ctx.channel.send(f"{user.mention}", embed=success)
        
        #update verified csv:
        with open("verified.csv", "a") as file:
            file.write(f"{user.display_name},{user.id},"+ ','.join(dat).replace("\n", "") + ",verified\n")
        file.close()
        
        #finally add roles after verifying user
        verified_role = discord.utils.get(user.guild.roles, name = "Verified")
        await user.add_roles(verified_role)

@client.command(aliases = ["info", "i"])
async def _info(ctx, member):
    user_info = ["Member", "MemberId","PRN", "SRN", "Semester", "Section", "Hostelite", "Stream/Campus", "Stream", "Campus", "verified"]
    in_e = discord.Embed(title = "User Info", color = 0x48bf91)

    try:
        user = await commands.MemberConverter().convert(ctx, member)
        data = getverified(str(user.id))
        if "unverified" in data:
            await ctx.channel.send(f"{ctx.author.mention} The user has not been verified yet")
            return

        for i in range(len(user_info)):
            in_e.add_field(name=user_info[i], value=data[i])
        await ctx.channel.send(embed=in_e)
       
    except:
        await ctx.channel.send(f"{ctx.author.mention} enter a valid member")

@client.command(aliases = ["f", "file"])
async def _file(ctx):
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    mods = discord.utils.get(ctx.guild.roles, name="Moderators")
    bb = discord.utils.get(ctx.guild.roles, name="Bot Bosses")

    if (admin in ctx.author.roles) or (mods in ctx.author.roles) or (bb in ctx.author.roles):
        await ctx.channel.send("You have the necesarry role")
        with open("verified.csv", "r") as fp:
            await ctx.channel.send(file=discord.File(fp, 'verified.txt'))
    else:
        await ctx.channel.send("You are not authorised to do that")


client.run(token)
