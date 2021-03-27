import discord
import random
from discord.ext import commands
from discord import Embed, Member
from discord.utils import get
from discord.ext.commands import has_permissions

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.colors = [discord.Color.default(),
                    discord.Color.teal(),
                    discord.Color.dark_teal(),
                    discord.Color.green(),
                    discord.Color.dark_green(),
                    discord.Color.blue(),
                    discord.Color.purple(),
                    discord.Color.dark_purple(),
                    discord.Color.magenta(),
                    discord.Color.dark_magenta(),
                    discord.Color.gold(),
                    discord.Color.dark_gold(),
                    discord.Color.orange(),
                    discord.Color.dark_orange(),
                    discord.Color.red(),
                    discord.Color.dark_red()]
    
    @commands.command(pass_context = True, aliases=['crole'])
    @has_permissions(manage_roles=True)
    async def create_role(self, ctx, _role):
        guild = ctx.guild
        if get(guild.roles, name=_role):
            embed=discord.Embed(title="Role ERROR", description=f"{ctx.message.author.mention} this role already exist", color=0xff00f6)
            await ctx.send(embed=embed)
        else:
            await guild.create_role(name=_role, colour=random.choice(self.colors))
            embed=discord.Embed(title="Role Created", description=f"{ctx.message.author.mention} created `{_role}` role", color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"{ctx.message.author} created {_role} role")

    @create_role.error
    async def crole_error(self, ctx ,error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("No permission to create a role")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Input ERROR", description=f"{ctx.message.author.mention} Arguments are missing", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Role missing")
        
    @commands.command(pass_context = True)
    @has_permissions(manage_roles=True)
    async def drole(self, ctx, *, role: discord.Role):
        if role is None:
            embed=discord.Embed(title="Remove Role Error", description=f"{ctx.message.author.mention} Please add a role", color=0xff00f6)
            await ctx.send(embed=embed)
        else:
            await role.delete()
            embed=discord.Embed(title="Remove role", description=f"{ctx.message.author.mention} Successfully removed `{role}` role from server", color=0xff00f6)
            await ctx.send(embed=embed)
    @drole.error
    async def drole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("No permission to delete a role")

    @commands.command(pass_context = True, aliases=['role'])
    @has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        if role in user.roles:
            embed=discord.Embed(title="Add Role Error", description=f"{user.mention} already have this role {role.mention}", color=0xff00f6)
            await ctx.send(embed=embed)
        else:
            await user.add_roles(role)
            embed=discord.Embed(title="Add Role", description=f"{ctx.message.author.mention} Successfully given {role.mention} role to {user.mention}", color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"{ctx.message.author} changed role to {user}")
    
    #ERROR HANDLING 
    @addrole.error
    async def addrole_error(self, ctx ,error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("No permission to give a role")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Input ERROR", description=f"{ctx.message.author.mention} Arguments are missing", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Role or Username missing")
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="Input ERROR", description=f"{ctx.message.author.mention} Bad syntax", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Bad syntax for roles")
        elif isinstance(error, commands.CheckFailure):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} You are lacking a required role", color=0xff00f6)
            await ctx.send(embed=embed)
            print("No role")
        
    @commands.command(pass_context = True)
    @has_permissions(manage_roles=True)
    async def rmrole(self, ctx, role: discord.Role, user: discord.Member):
        if role not in user.roles:
            embed=discord.Embed(title="Remove Role Error", description=f"{user.mention} is not {role.mention}", color=0xff00f6)
            await ctx.send(embed=embed)
        else:
            await user.remove_roles(role)
            embed=discord.Embed(title="Remove role", description=f"{ctx.message.author.mention} Successfully removed {role.mention} role from {user.mention}", color=0xff00f6)
            await ctx.send(embed=embed)
    
    #ERROR HANDLING 
    @rmrole.error
    async def rmrole_error(self, ctx ,error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Cant remove a role")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Input ERROR", description=f"{ctx.message.author.mention} Arguments are missing", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Role or Username missing")
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="Input ERROR", description=f"{ctx.message.author.mention} Bad syntax", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Bad syntax for roles")
        elif isinstance(error, commands.CheckFailure):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} You are lacking a required role", color=0xff00f6)
            await ctx.send(embed=embed)
            print("No role")

def setup(client):
    client.add_cog(Roles(client))