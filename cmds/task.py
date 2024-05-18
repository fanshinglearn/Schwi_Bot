import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, datetime
from crawler.towerofsaviors import TowerOfSaviors
from crawler.opgg import InGame

class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('setting.json', 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        test_channel = self.bot.get_channel(int(jdata['channel']['test_channel']))

        # 神魔之塔
        async def towerofsaviors():
            await self.bot.wait_until_ready()
            towerofsaviors_channel = self.bot.get_channel(int(jdata['channel']['towerofsaviors_channel']))
            
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%M')
                digit = int(now_time[1])
                
                # 00 10 20 30 40 50
                if digit == 0:
                    # tos_jdata
                    with open('data/towerofsaviors.json', 'r', encoding='utf8') as jfile:
                        tos_jdata = json.load(jfile)
                    
                    tos = TowerOfSaviors()
                    
                    # 新聞稿
                    tos.get_news()
                    if tos.titles[0] != tos_jdata['latest_news']:
                        # embed
                        embed=discord.Embed(title=tos.titles[0], url=tos.urls[0])
                        embed.set_image(url=tos.img_urls[0])
                        await towerofsaviors_channel.send(embed=embed)
                    tos_jdata['latest_news'] = tos.titles[0]
                    
                    # 慶祝活動
                    tos.get_announcement()
                    if tos.titles[0] != tos_jdata['latest_announcement']:
                        # embed
                        embed=discord.Embed(title=tos.titles[0], url=tos.urls[0])
                        embed.set_image(url=tos.img_urls[0])
                        await towerofsaviors_channel.send(embed=embed)
                    tos_jdata['latest_announcement'] = tos.titles[0]
                    
                    # 存檔
                    with open('data/towerofsaviors.json', 'w', encoding='utf8') as jfile:
                        json.dump(tos_jdata, jfile, ensure_ascii=False, indent=4)
                    
                    await asyncio.sleep(500)
                else:
                    await asyncio.sleep(10)
        
        # OPGG
        async def opgg_in_game():
            await self.bot.wait_until_ready()
            opgg_channel = self.bot.get_channel(int(jdata['channel']['opgg_channel']))

            while not self.bot.is_closed():
                with open('data/opgg/player.json', 'r', encoding='utf8') as jfile:
                    player_jdata = json.load(jfile)
                
                # 稽查是否在遊戲中
                dc_msg = ''
                game_type = None

                for player in player_jdata['player']:
                    in_game = InGame(player['player_id'])
                    if in_game.is_in_game:
                        # 在遊戲中!!
                        if in_game.game_id != player['last_game_id']:
                            # 新遊戲!!
                            print(f'{player["player_name"]} 開始了新遊戲!! 遊戲模式: {in_game.game_type}')
                            player['last_game_id'] = in_game.game_id

                            dc_msg += f'<@{player["dc_id"]}> '
                            game_type = in_game.game_type

                if dc_msg:
                    if game_type == '隨機單中':
                        game_type = '單中'
                    elif game_type == '單/雙排積分':
                        game_type = '單雙'
                    elif game_type == '彈性積分':
                        game_type = '彈積'
                    dc_msg += f'{game_type}不揪'
                    await opgg_channel.send(dc_msg)
                    with open('data/opgg/player.json', 'w', encoding='utf8') as jfile:
                        json.dump(player_jdata, jfile, ensure_ascii=False, indent=4)
                    
                await asyncio.sleep(10)
        
        self.bg_task = self.bot.loop.create_task(towerofsaviors())
        self.bg_task = self.bot.loop.create_task(opgg_in_game())
    
    # @commands.command()
    # async def set_channel(self, ctx, ch: int):
    #     self.channel = self.bot.get_channel(ch)
    #     await ctx.send(f'Set Channel: {self.channel.mention}')
    
    # @commands.command()
    # async def set_time(self, ctx, time):
    #     self.counter = 0
    #     with open('setting.json', 'r', encoding='utf8') as jfile:
    #         jdata = json.load(jfile)
        
    #     jdata['time'] = time

    #     with open('setting.json', 'w', encoding='utf8') as jfile:
    #         json.dump(jdata, jfile, indent=4)


async def setup(bot):
    await bot.add_cog(Task(bot))