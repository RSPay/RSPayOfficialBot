import discord
from discord.ext import commands, tasks

import logging
import aiohttp
import asyncio

import config

class RSPayBot(commands.AutoShardedBot):
    
    def __init__(self):
        intents = discord.Intents.all()
        self.config = __import__("config")
        super().__init__(command_prefix=config.PREFIX, description="RSPay OfficialBot provided by RisuPu",
                        intents=intents, shard_count=config.SHARD_COUNT)
        
        #logging
        self.logging = logging.getLogger("discord")
        logging.basicConfig(level=logging.WARNING, format="[DebugLog] %(levelname)-8s: %(message)s")
        
        #aiohttp
        self.session = aiphttp.ClientSession(loop=self.loop)
        
        if str(type(config.OWNERS)) == "<class 'int'>":
            self.owner_id = config.OWNERS
            self.owner_ids = None
        elif str(type(config.OWNERS)) == "<class 'list'>":
            self.owner_id = None
            self.owner_ids = config.OWNERS
        elif str(type(config.OWNERS)) == "<class 'tuple'>":
            self.owner_id = None
            self.owner_ids = config.OWNERS
        else:
            self.owner_id = None
            self.owner_ids = None
            print("[System] Failed to set owner_ids / owner_id.")
       
    EXTENSIONS = config.EXTENSIONS
    
    async def on_ready(self):
        asyncio.gather(self.change_presence(activity=discord.Game(f"{config.PREFIX}help | Guidls: {len(self.guilds)} Users: {len(self.users)} | RSPay OfficialBot provided by RisuPu")))
        print("[System] Enabled RSPayBot")
        
    async def on_connect(self):
        print("[System] Connected.")
        
        try:
            self.remove_command("help")
        except Exception as e:
            print(f"[System] Default help command remove failed. → {e}")
        else:
            print(f"[System] Default help command removed.")
        
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"[System] {extension} load failed. → {e}")
            else:
                print(f"[System] {extension} load.")
    
        asyncio.gather(self.change_presence(activity=discord.Game("Enabling RSPayOfficialBot | Please wait...")))
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            e = discord.Embed(title="Error | DisabledCommand", description="このコマンドは管理者によって無効化されています。", timestamp=ctx.message.created_at)
            asyncio.gather(ctx.send(embed=e))
        elif isinstance(error, commands.NotOwner):
            e = discord.Embed(title="Error | NotOwner", description="このコマンドは管理者のみが使用できます。", timestamp=ctx.message.created_at)
            asyncio.gather(ctx.send(embed=e))
        elif isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(title="Error | CommandOnCooldown", description=f"クールダウン中です。 {str(error.retry_after)[0:4]}秒後に再実行可能です。", timestamp=ctx.message.created_at)
            asyncio.gather(ctx.send(embed=e))
        else:
            e = discord.Embed(title="Error | Unknown", description=f"```py\n{error}\n```", timestamp=ctx.message.created_at)
            asyncio.gather(ctx.send(embed=e))
    
    async def close(self):
        tasks = [super().close(), self.session.close()]
        asyncio.gather(*tasks)
    
    def run(self):
        try:
            super().run(config.BOT_TOKEN, reconnect=True)
        except Exception as e:
            print(f"[Error] Cannot run bot. → {e}")

bot = RSPayBot()

print("[System] Enabling RSPayBot...")
bot.run(bot.http.token)