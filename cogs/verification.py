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

    @commands.command(aliases=["v", "verify", "V"])
    async def _verify(self, ctx, SRN=""):
        # embed variables
        success = discord.Embed(title="Success", color=0x00FF00)
        fail = discord.Embed(title="Fail", color=0xFF0000)
        veri = discord.Embed(
            title="Verification",
            description="SRN & PRN Verification process",
            color=0x0000FF,
        )
        veri.add_field(
            name="Process",
            value="1. Enter SRN (PES1UG19.....) as argument\n2. Enter PRN(PES12019.....) as text when promted by bot",
        )
        user = ctx.author

        # help for verification:
        if ("help" in SRN) or (SRN==""):
            await ctx.channel.send(embed=veri)
            return

        # checking if user entered PSN and not SRN
        if ("PES12020" in SRN) or ("PES22020" in SRN) or ("PES12019" in SRN) or ("PES22019" in SRN):
            veri.add_field(name="No SRN found", value="Enter SRN and not PRN as argument")
            await ctx.channel.send(f"{user.mention}", embed=veri)
            return

        # getting creds from pesu academy
        dat = self.getuser(SRN)

        if "Done" in dat:
            await ctx.channel.send(f"{user.mention} you have already been verified")
            await ctx.channel.send(f"To avoid spamming we allow only one account per user")
            await ctx.channel.send(
                f"If you think someone else has used your SRN, please ping `@Bot Dev` or `@Admin` without fail"
            )
            return
            # Just in case

        # checking if the value returned from pesu academy is an error
        if "error" in dat:
            fail.add_field(name="Invalid SRN", value=f"SRN ({SRN}) not found")
            await ctx.send(f"{user.mention}", embed=fail)
            await ctx.send(
                "`Note: There are a lot of discrepancies in the fresher's list of SRNs. If there's an issue, do ping @Bot Dev or @Admin`"
            )
            return
        else:
            if ("PES12018" in SRN):
                await ctx.channel.send(f"{user.mention}, now enter your section to complete verification")
                msg = await self.client.wait_for("message", check=lambda msg: msg.author == ctx.author)
                msg = str(msg.content)
                msg = "Section " + msg.upper()
                if msg != dat[3]:
                    fail.add_field(
                        name="Section validation failed",
                        value=f"{msg} entered does not match the corresponding SRN {SRN}"
                    )
                    await ctx.channel.send(f"{user.mention}", embed=fail)
                    sleep(5)
                    await ctx.channel.purge(limit=4)
                    return
                senior_role = discord.utils.get(user.guild.roles, name="Seniors")
                await user.add_roles(senior_role)
            
            else:
                # if valid creds are returned from pesu academy
                await ctx.channel.send(
                    f"{user.mention}, now enter PRN to complete verification"
                )
                msg = await self.client.wait_for(
                    "message", check=lambda msg: msg.author == ctx.author
                )
                if msg.content != dat[0]:
                    fail.add_field(
                        name="PRN validation failed",
                        value=f"PRN ({msg.content}) entered did not match the corresponding SRN ({SRN})",
                    )
                    await ctx.channel.send(f"{user.mention}", embed=fail)
                    sleep(5)
                    await ctx.channel.purge(limit=4)
                    return

                if dat[2] == "Sem-3":
                    role_str = (
                        dat[-3]
                        .replace("Campus", "")
                        .replace(" ", "")
                        .replace("BIOTECHNOLOGY", "BT")
                    )
                elif dat[2] == "Sem-1":
                    role_str = dat[-2] + "(Junior)"
                if role_str not in [r.name for r in ctx.guild.roles]:
                    for each_role in ctx.guild.roles:
                        if each_role.name == "Admin":
                            admin = each_role
                    await ctx.channel.send(
                        f"{user.mention} Looks like your role isn't on the server yet. DM or tag {admin.mention}"
                    )
                    return
                else:
                    role = discord.utils.get(user.guild.roles, name=role_str)
                    await user.add_roles(role)

            for i in range(8):
                success.add_field(name="{0}".format(data_list[i]), value=dat[i])
            await ctx.channel.send(f"{user.mention}", embed=success)

            # update verified csv:
            with open("verified.csv", "a") as file:
                file.write(
                    f"{user.display_name},{user.id},"
                    + ",".join(dat).replace("\n", "")
                    + ",verified\n"
                )

            # finally add roles after verifying user
            verified_role = discord.utils.get(user.guild.roles, name="Verified")
            await user.add_roles(verified_role)
            justjoined_role = discord.utils.get(user.guild.roles, name="Just Joined")
            await user.remove_roles(justjoined_role)

            sleep(5)
            await ctx.channel.purge(limit=4)
        await self.client.get_channel(BOT_LOGS).send(f"{user.mention}", embed=success)


def setup(client):
    client.add_cog(verify(client))