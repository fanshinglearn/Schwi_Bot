import discord
from discord.ext import commands
import json, asyncio, random
from pypinyin import pinyin, Style
from core.classes import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
    def compare_pinyin(self, my_word, msg):
        my_pinyin = pinyin(my_word, style=Style.NORMAL)
        for word in msg:
            if my_pinyin == pinyin(word, style=Style.NORMAL):
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author != self.bot.user:
            # 休比
            if self.compare_pinyin('休', msg.content) and self.compare_pinyin('比', msg.content):
                # embed
                embed=discord.Embed(title=msg.content, color=0x5b6db3)
                if msg.author.avatar:
                    embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)
                else:
                    embed.set_author(name=msg.author.display_name)
                
                # 爆了?
                die_words = jdata['keyword']['die']
                word_found = False
                for word in die_words:
                    if self.compare_pinyin(word, msg.content):
                        await msg.delete()
                        embed.set_footer(text="已刪除訊息", icon_url=self.bot.user.avatar.url)
                        word_found = True
                        ridicule_words = jdata['keyword']['ridicule_words']
                        ridicule_word = random.choice(ridicule_words)
                        await msg.channel.send(ridicule_word)
                        await asyncio.sleep(1)
                        await msg.channel.purge(limit=1)
                        break
                if not word_found:
                    embed.set_footer(text="叫我?", icon_url=self.bot.user.avatar.url)

                # print_channel
                print_channel = self.bot.get_channel(int(jdata['channel']['print_channel']))
                await print_channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Event(bot))