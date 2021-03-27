import discord
import asyncio
from discord.ext import commands
from discord import Embed, Member

class Levels(commands.Cog):
    def __init__(self,client):
        self.client = client

    async def level_up(self, user):
        cur_xp = user['xp']
        cur_level = user['level']

        if cur_xp >= round((4 * (cur_level ** 3)) / 5):
            await self.client.pg_con.execute("UPDATE users SET level = $1 WHERE user_id = $2 AND guild_id = $3", cur_level + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        
        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        
        if not user:
            await self.client.pg_con.execute("INSERT INTO users (user_id, guild_id, level, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)

        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)
        
        if await self.level_up(user):
            embed=discord.Embed(title=" :arrow_up: Level Up :arrow_up: ", description="**{0}** is now level **{1}**!".format(message.author.mention, user['level'] + 1), color=0x00ffff)
            await message.channel.send(embed=embed)
            print(f"{message.author} level up ")
        
    @commands.command(pass_context = True)
    async def level(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            await ctx.send(f"{member.mention} doesn't have level")

        else:
            embed = discord.Embed(color=0x29aff2, timestamp=ctx.message.created_at)
            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
            embed.add_field(name="Level", value=user[0]['level'])
            embed.add_field(name="Total XP", value=user[0]['xp'])
            embed.add_field(name="XP to next Level", value=((round((4 * (user[0]['level'] ** 3)) / 5)) - (user[0]['xp'])), inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Levels(client))