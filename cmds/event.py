import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, msg):

        if msg.author != self.bot.user:
            schwi = jdata['keyword']['schwi']
            die = jdata['keyword']['die']
            
            if any(word in msg.content for word in schwi):
                print_channel = self.bot.get_channel(int(jdata['Print_Channel']))

                if any(word in msg.content for word in die):
                    await msg.delete()
                    await print_channel.send(f'----- 已刪除訊息 -----\n{msg.author.mention}:\n> {msg.content}\n')
                else:
                    await print_channel.send(f'----- 提到休比 -----\n{msg.author.mention}:\n> {msg.content}\n')


async def setup(bot):
    await bot.add_cog(Event(bot))