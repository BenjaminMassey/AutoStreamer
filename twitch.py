from twitchio.ext import commands

import settings

class TwitchBot(commands.Bot):

    filename = ""

    def __init__(self, auth, channel, filename):
        super().__init__(
            token=auth,
            prefix='?',
            initial_channels=[channel]
        )
        self.filename = filename

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        
        user = str(message.author.name)
        msg = str(message.content)
        
        file = open(self.filename, "w")
        file.write(user + " ::: " + msg)
        file.close()
        
        print(user + " says '" + msg + "'.")
        
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

app_settings = settings.Settings()
auth = app_settings.get("twitch_auth")
channel = app_settings.get("twitch_channel")

filename = "latest.txt"

bot = TwitchBot(auth, channel, filename)

print("Twitch Bot is set up!")

bot.run()