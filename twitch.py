from twitchio.ext import commands
import threading, asyncio

class TwitchBot(commands.Bot):

    latest = ("", "")

    def __init__(self, auth, channel):
        super().__init__(
            token=auth,
            prefix='?',
            initial_channels=[channel]
        )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        
        user = str(message.author.name)
        msg = str(message.content)

        self.latest = (user, msg)
        
        print(user + " says '" + msg + "'.")
        
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

class TwitchThread(threading.Thread):
    
    def __init__(self, auth, channel):
        threading.Thread.__init__(self)
        self.bot = TwitchBot(auth, channel)
        
    def run(self):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.run())
        except:
            pass
