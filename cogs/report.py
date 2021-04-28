import discord
import asyncio
from discord.ext import commands
from discord import Embed, Member

class Report(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True, aliases=['rep'])
    async def report(self, ctx, member: discord.Member, *reason:str):
        warn_embed = discord.Embed(
        title=":warning: User Report :warning:",
        colour=0xFF0000)
        warn_user = discord.Embed(
            title=":white_check_mark: User Report :white_check_mark:",
            colour=0x40E0D0)
        if not reason:
            await ctx.send(f"{ctx.message.author.mention} Please provide a reason!")
            return
        reason = ' '.join(reason)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            await self.client.pg_con.execute("INSERT INTO reports (user_id, report) VALUES($1, ARRAY[$2])", member_id, reason)
            warn_user.add_field(name="Report Committed", value=f"{ctx.message.author.mention} report for the user {member.mention} commited", inline=False)
            await ctx.send(embed=warn_user)
            print("report committed")
        else:
            await self.client.pg_con.execute("UPDATE reports SET report = array_append(report, $1) WHERE user_id = $2", reason, member_id)
            warn_user.add_field(name="Report Committed", value=f"{ctx.message.author.mention} report for the user {member.mention} commited", inline=False)
            await ctx.send(embed=warn_user)
            print("report committed")
        
        channel = self.client.get_channel(802344348825157632)
        warn_embed.add_field(name="Report Committed", value=f"{ctx.message.author.mention} reported the user {member.mention}", inline=False)
        warn_embed.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=warn_embed)
        
    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Argument missing for reports")
    
    @commands.command(pass_context = True, aliases=['drep'])
    @commands.has_permissions(kick_members=True)
    async def dreport(self, ctx, member:discord.Member):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
            member_id = str(member.id)
            await self.client.pg_con.execute("DELETE FROM reports WHERE user_id = $1", member_id)
            drep_embed.add_field(name="Report Cleared", value=f"{ctx.message.author.mention} removed reports from {member.mention}", inline=False)
            await ctx.send(embed=drep_embed)
            print("removed reports from user {0}".format(member))
       
    @dreport.error
    async def dreport_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to remove Report")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description=f"{ctx.message.author.mention} Specify the user!", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Missing argument about dreport")

    @commands.command(pass_context = True)
    async def reports(self, ctx, member: discord.Member):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            array_len = await self.client.pg_con.fetch("SELECT array_length(report, 1) FROM reports WHERE user_id = $1", member_id)
            temp_string = str(array_len)
            total_reports = ''.join(filter (lambda i: i.isdigit(), temp_string)) 
            drep_embed.add_field(name="Reports History", value=f"{member.mention} Has **{str(total_reports)}** reports in history", inline=False)
            await ctx.send(embed=drep_embed)
            return
    
    @reports.error
    async def reports_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description=f"{ctx.message.author.mention} Specify the user!", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Specify the user abour report history")

def setup(client):
    client.add_cog(Report(client))                
