import discord
from discord.ext import commands

class verify(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.datalist = ["PRN", "SRN", "Semester", "Section", "Hostelite", "Stream/Campus", "Stream", "Campus"]

    
    def getuser(self, a=""):
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

    @commands.command(aliases = ['v', 'verify'])
    async def _verify(self, ctx, SRN):
        #embed variables
        success = discord.Embed(title = "Success", color = 0x00ff00)
        fail = discord.Embed(title = "Fail", color = 0xff0000)
        veri = discord.Embed(title="Verification", description="SRN & PRN Verification process",color = 0x0000ff)
        veri.add_field(name="Process", value="1. Enter SRN (PES1UG19.....) as argument\n2. Enter PRN(PES12019.....) as text when promted by bot")
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
        dat = self.getuser(SRN)

        if "Done" in dat:
            await ctx.channel.send(f"{user.mention} you have already been verified")
            await ctx.channel.send(f"To avoid spamming we allow only one account per user")
            await ctx.channel.send(f"If you think someone else has used your SRN, please ping `@Bot Dev` or `@Admin` without fail")    
            return
            # Just in case

        #checking if the value returned from pesu academy is an error
        if "error" in dat:
            fail.add_field(name = "Invalid SRN", value=f"SRN ({SRN}) not found")
            await ctx.send(f"{user.mention}", embed=fail)
            return
        else:
            #if valid creds are returned from pesu academy
            await ctx.channel.send(f"{user.mention}, now enter PRN to complete verification")
            msg = await self.client.wait_for('message', check = lambda msg: msg.author == ctx.author)
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
                success.add_field(name="{0}".format(self.data_list[i]), value = dat[i])
            await ctx.channel.send(f"{user.mention}", embed=success)

            #update verified csv:
            with open("verified.csv", "a") as file:
                file.write(f"{user.display_name},{user.id},"+ ','.join(dat).replace("\n", "") + ",verified\n")

            #finally add roles after verifying user
            verified_role = discord.utils.get(user.guild.roles, name = "Verified")
            await user.add_roles(verified_role)

            for i in range(100000000):
                pass
            await ctx.channel.purge(limit=5)
        
def setup(client):
    client.add_cog(verify(client))