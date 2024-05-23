import datetime
import discord
from discord.ext import commands
from core.classes import Cog_Extension
from crawler.opgg import InGame

class Main(Cog_Extension):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send('HELLO')
        await ctx.send('<@511899806826758148>')
    
    @commands.command()
    async def em(self, ctx):
        in_game = InGame('')
        in_game.get_team_data()
        
        team_data = in_game.team_data


        
        embed=discord.Embed(title='積分對戰', color=0x5383e8,
                            timestamp=datetime.datetime.now())
        if ctx.author.avatar:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        else:
            embed.set_author(name=ctx.author.display_name)
        
        embed.add_field(name="藍隊", value="111", inline=True)
        embed.add_field(name="紅隊", value="222", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        for i in range(5):
            for j in range(i, i+6, 5):
                game_name = team_data[j]['summoner']['game_name']
                max_word = 10
                if len(game_name) > max_word:
                    game_name = f'{game_name[:max_word]}...'

                tier_info = team_data[j]['summoner']['tier_info']
                tier = f'> <:paimoncry:1024627970360479744> {tier_info["tier"]} {tier_info["division"]}' if tier_info else ''

                embed.add_field(name=game_name, value=tier, inline=True)
            embed.add_field(name="\u200b", value="\u200b\n\u200b", inline=True)
        
        embed.set_footer(text="休比", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        # await ctx.send(team_data)
        # await ctx.send('<:paimoncry:1024627970360479744>')
    
    # @commands.command()
    # async def c(self, ctx, *, msg):
    #     guild = ctx.guild
    #     with open('path/to/your/yasuo.jpg', 'rb') as image_file:  # 替换为你的 JPG 文件路径
    #         image_data = image_file.read()
    #         emoji = await guild.create_custom_emoji(name='yasuo', image=image_data)
    #         created_emojis.append(emoji)
    #         print(f'Created emoji: {emoji.name}')
    #     await ctx.send(f'Created emoji: {emoji.name}')

    @commands.command()
    async def sayd(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)
    
    @commands.command()
    async def clean(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)


async def setup(bot):
    await bot.add_cog(Main(bot))